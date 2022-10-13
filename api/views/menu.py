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
    output = {}
    item_genres = ItemGenre.objects.all()
    output['genres'] = [0] * len(item_genres)
    for i, item_genre in enumerate(item_genres):
        output['genres'][i] = {
            'genre_id': item_genre.id,
            'genre_name': item_genre.genre_name,
        }
        
        items = Item.objects.filter(genre_id=item_genre.id)
        output['genres'][i]['items'] = [0] * len(items)
        for j, item in enumerate(items):
            output['genres'][i]['items'][j] = {
                'item_id': item.id,
                'item_name': item.item_name,
                'price': item.price,
            }

            available_options = AvailableOption.objects.filter(item_id=item.id)
            output['genres'][i]['items'][j]['available_options'] = [0] * len(available_options)
            for k, available_option in enumerate(available_options):
                print(available_option.option_id)
                option = available_option.option_id
                output['genres'][i]['items'][j]['available_options'][k] = {
                    'option_id': option.id,
                    'option_name': option.option_name,
                }
        
    return JsonResponse(output, status=200)