import asynctest
import asyncio
from asynctest import mock, patch
from ..client import GraphClient
from ..constants import *
from ..exceptions import *
import requests


class TestClient(asynctest.TestCase):
    _test_app_id = None
    _test_app_secret = None
    _test_tenant_id = None
    _token = None
    _user_id = None

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls._test_app_id = "dd8b55a2-c72e-47ab-a2a4-13660159883a"
        cls._test_app_secret = "5z2_33Y2aEdG-22MBja~u0o.3-Asg884KG"
        cls._test_tenant_id = "31bd24f9-0587-41a2-b713-98deb6cd245d"
        cls._user_id = "edce4f8e-92d6-48be-8f8d-1acbfd1293ed"

        token_params = {
            'grant_type': 'client_credentials',
            "scope": "https://graph.microsoft.com/.default",
            'client_id': cls._test_app_id,
            'client_secret': cls._test_app_secret,
        }

        r = requests.post(f"https://login.microsoftonline.com/{cls._test_tenant_id}/oauth2/v2.0/token",
                          data=token_params)
        res_json = r.json()
        cls._token = res_json['access_token']

    def get_instance(self):
        return GraphClient(enable_logging=True)

    async def test_list_users_manual_token(self):
        i = self.get_instance()
        res, status = await i.list_users(token=TestClient._token)
        self.assertEqual(1, len(res["value"]))

    async def test_list_users_managed_token(self):
        i = self.get_instance()
        await i.manage_token(TestClient._test_app_id, TestClient._test_app_secret, TestClient._test_tenant_id)
        res, status = await i.list_users()
        self.assertEqual(1, len(res["value"]))

    async def test_manage_token(self):
        i = self.get_instance()
        await i.manage_token(TestClient._test_app_id, TestClient._test_app_secret, TestClient._test_tenant_id)
        self.assertEqual(True, i.is_managed)
        token = i.token
        self.assertIsNotNone(token)

    async def test_manage_token_refreshing(self):
        i = self.get_instance()
        i._token_refresh_interval_sec = 5
        await i.manage_token(TestClient._test_app_id, TestClient._test_app_secret, TestClient._test_tenant_id)
        self.assertEqual(True, i.is_managed)
        token1 = i.token
        self.assertIsNotNone(token1)
        await asyncio.sleep(7)
        token2 = i.token
        self.assertIsNotNone(token2)
        self.assertNotEqual(token1, token2)

    async def test_get_user(self):
        i = self.get_instance()
        res, status = await i.get_user(TestClient._user_id, token=TestClient._token)
        self.assertEqual(status, HTTPStatus.OK)

    async def test_acquire_token(self):
        i = self.get_instance()
        token, status = await i.acquire_token(TestClient._test_app_id, TestClient._test_app_secret, TestClient._test_tenant_id)
        self.assertEqual(status, HTTPStatus.OK)
        self.assertIsNotNone(token["access_token"])

    @asynctest.skip("need real application")
    async def test_create_subscription(self):
        i = self.get_instance()
        res, status = await i.list_users(token=TestClient._token)
        user_id = res["value"][0]["id"]
        try:
            res = await i.create_subscription(
                "created", "https://mila.bitdam.com/api/v1.0/office365/notification",
                SubscriptionResourcesTemplates.Mailbox, 10,
                user_id=user_id, token=TestClient._token)
        except Unauthorized as e:
            pass

    @asynctest.skip("soon")
    async def test_throttling(self):
        i = self.get_instance()
        loop = asyncio.get_event_loop()
        try:
            # res, status = await i.list_users(token=TestClient._token)
            results = await asyncio.gather(*[i.get_user(user_id=TestClient._user_id, token=TestClient._token) for _ in range(1000)])
        except Exception as e:
            print(str(e))
            self.fail(str(e))

        for i, result in enumerate(results):
            self.assertEqual(result[1], HTTPStatus.OK)
