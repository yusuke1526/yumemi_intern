import os
import json
from pathlib import Path

from django.test import Client, TestCase

from ..models import ItemGenre, Item, Option, AvailableOption

current_dir = Path(__file__).resolve().parent

# Create your tests here.
class GetClientsMenuTests(TestCase):
    # テスト用データベースの初期化
    def setUp(self):
        item_genres = ['握り', '軍艦', 'サイドメニュー', 'ドリンク']
        item_genres = [ItemGenre(genre_name=name) for name in item_genres]
        ItemGenre.objects.bulk_create(item_genres)

        items = [
            (item_genres[0], 'まぐろ', 200),
            (item_genres[0], 'サーモン', 180),
            (item_genres[1], 'いくら', 300),
            (item_genres[2], 'から揚げ', 350),
            (item_genres[3], 'ウーロン茶', 100)
        ]
        items = [Item(genre_id=genre_id, item_name=name, price=price) for genre_id, name, price in items]
        Item.objects.bulk_create(items)

        options = ['わさび', '特大', 'チリソース', 'マヨネーズ']
        options = [Option(option_name=name) for name in options]
        Option.objects.bulk_create(options)

        available_options = [
            (items[0], options[0]),
            (items[0], options[1]),
            (items[1], options[0]),
            (items[1], options[1]),
            (items[3], options[2]),
            (items[3], options[3]),
        ]
        available_options = [AvailableOption(item_id=item_id, option_id=option_id) for item_id, option_id in available_options]
        AvailableOption.objects.bulk_create(available_options)

    def test_client_menu_correct(self):
        response = Client().get('/clients/menu', content_type='application/json')
        data = json.loads(response.content)
        with open(os.path.join(current_dir, 'test_jsons/client_menu_correct.json'), 'r') as f:
            ans = json.load(f)
        self.assertEqual(data, ans)