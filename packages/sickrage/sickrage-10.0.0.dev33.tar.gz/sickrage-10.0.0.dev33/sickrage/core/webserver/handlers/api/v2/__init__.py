# ##############################################################################
#  Author: echel0n <echel0n@sickrage.ca>
#  URL: https://sickrage.ca/
#  Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#  -
#  This file is part of SiCKRAGE.
#  -
#  SiCKRAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  SiCKRAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################
import json
import os
import traceback
from abc import ABC

from tornado.escape import json_decode
from tornado.web import HTTPError

import sickrage
from sickrage.core.enums import ProcessMethod
from sickrage.core.helpers import get_internal_ip, get_external_ip
from sickrage.core.webserver.handlers.base import BaseHandler


class APIv2BaseHandler(BaseHandler, ABC):
    def prepare(self):
        super(APIv2BaseHandler, self).prepare()

        method_name = self.request.method.lower()
        if method_name == 'options':
            return

        certs = sickrage.app.auth_server.certs()
        auth_header = self.request.headers.get('Authorization')

        if auth_header:
            if 'bearer' in auth_header.lower():
                try:
                    token = auth_header.strip('Bearer').strip()
                    decoded_auth_token = sickrage.app.auth_server.decode_token(token, certs)

                    if not sickrage.app.config.user.sub_id:
                        sickrage.app.config.user.sub_id = decoded_auth_token.get('sub')
                        sickrage.app.config.save()

                    if sickrage.app.config.user.sub_id != decoded_auth_token.get('sub'):
                        return self.send_error(401, error='user is not authorized')

                    if sickrage.app.config.general.enable_sickrage_api and not sickrage.app.api.token:
                        exchanged_token = sickrage.app.auth_server.token_exchange(token)
                        if exchanged_token:
                            sickrage.app.api.token = exchanged_token

                    internal_connections = "{}://{}:{}{}".format(self.request.protocol,
                                                                 get_internal_ip(),
                                                                 sickrage.app.config.general.web_port,
                                                                 sickrage.app.config.general.web_root)

                    external_connections = "{}://{}:{}{}".format(self.request.protocol,
                                                                 get_external_ip(),
                                                                 sickrage.app.config.general.web_port,
                                                                 sickrage.app.config.general.web_root)

                    connections = ','.join([internal_connections, external_connections])

                    if sickrage.app.config.general.server_id and not sickrage.app.api.account.update_server(sickrage.app.config.general.server_id, connections):
                        sickrage.app.config.general.server_id = ''

                    if not sickrage.app.config.general.server_id:
                        server_id = sickrage.app.api.account.register_server(connections)
                        if server_id:
                            sickrage.app.config.general.server_id = server_id
                            sickrage.app.config.save()

                    self.current_user = decoded_auth_token
                except Exception:
                    return self.send_error(401, error='failed to decode token')
            else:
                return self.send_error(401, error='invalid authorization request')
        else:
            return self.send_error(401, error='authorization header missing')

    def get_current_user(self):
        return self.current_user

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.set_status(status_code)

        if status_code == 500:
            excp = kwargs['exc_info'][1]
            tb = kwargs['exc_info'][2]
            stack = traceback.extract_tb(tb)
            clean_stack = [i for i in stack if i[0][-6:] != 'gen.py' and i[0][-13:] != 'concurrent.py']
            error_msg = '{}\n  Exception: {}'.format(''.join(traceback.format_list(clean_stack)), excp)

            sickrage.app.log.debug(error_msg)
        else:
            error_msg = kwargs.get('reason', '') or kwargs.get('error', '')

        self.write_json({'error': error_msg})

    def set_default_headers(self):
        super(APIv2BaseHandler, self).set_default_headers()
        self.set_header('Content-Type', 'application/json')

    def write_json(self, response):
        self.write(json.dumps(response))

    def _parse_value(self, value, func):
        if value is not None:
            try:
                return func(value)
            except ValueError:
                raise HTTPError(400, f'Invalid value {value!r}')

    def _parse_boolean(self, value):
        if isinstance(value, str):
            return value.lower() == 'true'
        return self._parse_value(value, bool)


class PingHandler(APIv2BaseHandler, ABC):
    def get(self, *args, **kwargs):
        return self.write_json({'message': 'pong'})


class RetrieveSeriesMetadataHandler(APIv2BaseHandler, ABC):
    def get(self):
        series_directory = self.get_argument('seriesDirectory', None)
        if not series_directory:
            return self.send_error(400, error="Missing seriesDirectory parameter")

        json_data = {
            'rootDirectory': os.path.dirname(series_directory),
            'seriesDirectory': series_directory,
            'seriesId': '',
            'seriesName': '',
            'seriesProviderSlug': '',
            'seriesSlug': ''
        }

        for cur_provider in sickrage.app.metadata_providers.values():
            series_id, series_name, series_provider_id = cur_provider.retrieve_show_metadata(series_directory)

            if not json_data['seriesId'] and series_id:
                json_data['seriesId'] = series_id

            if not json_data['seriesName'] and series_name:
                json_data['seriesName'] = series_name

            if not json_data['seriesProviderSlug'] and series_provider_id:
                json_data['seriesProviderSlug'] = series_provider_id.slug

            if not json_data['seriesSlug'] and series_id and series_provider_id:
                json_data['seriesSlug'] = f'{series_id}-{series_provider_id.slug}'

        self.write_json(json_data)


class PostProcessHandler(APIv2BaseHandler, ABC):
    def get(self):
        path = self.get_argument("path", sickrage.app.config.general.tv_download_dir)
        force_replace = self._parse_boolean(self.get_argument("forceReplace", None) or False)
        return_data = self._parse_boolean(self.get_argument("returnData", None) or False)
        process_method = self.get_argument("processMethod", ProcessMethod.COPY.name)
        is_priority = self._parse_boolean(self.get_argument("isPriority", None) or False)
        delete = self._parse_boolean(self.get_argument("delete", None) or False)
        failed = self._parse_boolean(self.get_argument("failed", None) or False)
        proc_type = self.get_argument("type", 'manual')
        force_next = self._parse_boolean(self.get_argument("forceNext", None) or False)

        if not path and not sickrage.app.config.general.tv_download_dir:
            return self.send_error(400, error="You need to provide a path or set TV Download Dir")

        json_data = sickrage.app.postprocessor_queue.put(path, process_method=ProcessMethod[process_method.upper()], force=force_replace,
                                                         is_priority=is_priority, delete_on=delete, failed=failed, proc_type=proc_type, force_next=force_next)

        if 'Processing succeeded' not in json_data:
            return self.send_error(400, error=json_data)

        self.write_json({'data': json_data if return_data else ''})
