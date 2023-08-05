#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from typing import Dict, Any
from pywaclient.models.entity import Entity


class ManuscriptVersion(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)

    @property
    def title(self) -> str:
        return self._metadata['title']

    @property
    def state(self) -> str:
        """"""
        return self._metadata['state']


class ManuscriptExport(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        """

        :param client:
        :param metadata:
        """
        super().__init__(client, metadata)

    @property
    def manuscript(self) -> 'Manuscript':
        return Manuscript.from_id(self._client, self._metadata['manuscript']['id'])

    @property
    def version(self) -> ManuscriptVersion:
        return ManuscriptVersion(self._client, self._metadata['version'])

    @property
    def parts(self) -> Dict[str, Any]:
        return self._metadata['parts']


class Manuscript(Entity):

    @classmethod
    def from_id(cls, client: 'AragornApiClient', identifier: str):
        return Manuscript(client, client.manuscript.get(identifier))

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        """

        :param client:
        :param metadata:
        .:param author:
        """
        super().__init__(client, metadata)

    @property
    def title(self) -> str:
        """Title of the manuscript.

        :return: manuscript title
        """
        return self._metadata['title']

    @property
    def status(self) -> str:
        """The status of this manuscript (completed / ongoing).

        :return: status
        """
        return self._metadata['status']

    @property
    def author(self) -> 'User':
        """The author of this manuscript.

        :return: User
        """
        # this import is here because of circular imports.
        from pywaclient.models.user import User
        return User(self._client, self._metadata['author']['id'])

    @property
    def active_version(self) -> ManuscriptVersion:
        """Fetches the active version of this manuscript.

        :return: ManuscriptVersion
        """
        return ManuscriptVersion(self._client, self._metadata['active_version'][0])

    @property
    def active_export(self) -> ManuscriptExport:
        """Fetches the export of the active version of this manuscript.

        :return: ManuscriptExport
        """
        return ManuscriptExport(self._client, self._client.manuscript.export(self.id))
