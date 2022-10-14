import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from ..models import Order, OrderDetail, OrderedOption, Item, Table, Option, AvailableOption, ItemGenre

# Create your views here.
def clients_menu(request):
    '''
    商品一覧を取得する。

    Response
    200 OK
    {
        "genres": [
            {
                "genre_id": 1,
                "genre_name": "軍艦",
                "items": [
                    {
                        "item_id": 1,
                        "item_name": "いくらの軍艦",
                        "price": 10000,
                        "available_options": [
                            {
                                "option_id": 1,
                                "option_name": "チリソース"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    '''
    # genre, item, available_optionを全て取得
    item_genres_queryset = ItemGenre.objects.all()
    items_queryset = Item.objects.select_related("genre_id").all()
    available_options_queryset = AvailableOption.objects.select_related("item_id__genre_id", "option_id").all()

    # 整形しやすいようにkeyにidを持つdictionaryを作成
    genres = {item_genre.id: {"genre_id": item_genre.id, "genre_name": item_genre.genre_name, "items": {}} for item_genre in item_genres_queryset}

    for item in items_queryset:
        genre_id = item.genre_id.id
        genres[genre_id]["items"][item.id] = {"item_id": item.id, "item_name": item.item_name, "price": item.price, "available_options": []}

    for available_option in available_options_queryset:
        option = available_option.option_id
        item = available_option.item_id
        genre_id = item.genre_id.id
        item_id = item.id
        genres[genre_id]["items"][item_id]["available_options"].append({"option_id": option.id, "option_name": option.option_name})

    # JSONの形式に整形
    output = {"genres": list(genres.values())}
    for genre in output['genres']:
        genre['items'] = list(genre['items'].values())

    return JsonResponse(output, status=200)