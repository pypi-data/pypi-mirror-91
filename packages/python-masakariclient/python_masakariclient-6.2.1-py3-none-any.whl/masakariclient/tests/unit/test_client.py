# Copyright(c) 2016 Nippon Telegraph and Telephone Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_masakariclient
----------------------------------

Tests for `masakariclient` module.
"""
from unittest import mock

from masakariclient import client as mc
from masakariclient.common import utils
from masakariclient.tests import base


class FakeClient(object):

    def __init__(self, session):
        super(FakeClient, self).__init__()
        self.session = session


class TestMasakariclient(base.TestCase):

    @mock.patch.object(utils, 'import_versioned_module')
    def test_client_init(self, mock_import):
        the_module = mock.Mock()
        the_module.Client = FakeClient
        mock_import.return_value = the_module
        session = mock.Mock()

        res = mc.Client('FAKE_VER', session)

        mock_import.assert_called_once_with('FAKE_VER', 'client')
        self.assertIsInstance(res, FakeClient)
