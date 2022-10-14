import os
import json
from pathlib import Path

from django.test import Client, TransactionTestCase

from .utils import setup

test_json_dir = os.path.join(Path(__file__).resolve().parent, 'test_jsons/clients_menu/')

# Create your tests here.
class GetClientsMenuTests(TransactionTestCase):
    reset_sequences = True  # これを付けておくとauto incrementをリセットしてくれる
    
    # テスト用データベースの初期化
    def setUp(self):
        setup()

    def test_client_menu_correct(self):
        response = Client().get('/clients/menu', content_type='application/json')
        data = json.loads(response.content)
        with open(os.path.join(test_json_dir, 'correct.json'), 'r') as f:
            ans = json.load(f)
        self.assertEqual(data, ans)