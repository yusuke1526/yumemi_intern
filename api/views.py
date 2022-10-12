import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from .models import Order, OrderDetail, OrderedOption, Item, Table, Option, AvailableOption, ItemGenre

# Create your views here.
def healthcheck(request):
    return HttpResponse(status=200)

@csrf_exempt
def clients_orders(request):
    '''
    オーダーのリクエストをorders, order_details, ordered_optionsテーブルに登録する。

    Request Body:
    {
        "order_details": [
            {
                "item_id": 123,
                "options": [
                    {
                        "option_id": 1
                    }
                ]
            }
        ]
    }

    Response:
    201 Created
    {
        "ordered_at": "YYYY/mm/dd HH:mm",
        "order_details": [
            {
                "item": {
                    "item_id": 1,
                    "item_name": "dish name",
                    "price": 1234
                },
                "options": [
                    {
                        "option_id": 1,
                        "option_name": "チリソース"
                    }
                ]
            }
        ]
    }

    400 Bad Request
    {
        "message":"Missing required field item_id/order_items/option_id"
    }

    {
        "message":"Item/Option not found"
    }

    {
        "message":"Chosen option is unavailable for that item"
    }
    '''
    # リクエストを取得
    body = request.body.decode('utf-8')
    data = json.loads(body)
    try: order_details = data['order_details']
    except KeyError: return JsonResponse({"message": "Missing required field order_details"}, status=400)
    table = Table.objects.get(id=data['table_id'])

    order_details_objects = [0] * len(order_details)
    # DB登録前に全ての値をチェック
    for i, order_item in enumerate(order_details):
        order_detail = {}
        # item_idをチェック
        try:
            item = Item.objects.get(id=order_item['item_id'])
        except KeyError:
            return JsonResponse({"message": "Missing required field item_id"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Item not found"}, status=400)
        order_detail['item'] = item

        # optionsをチェック
        try: options = order_item['options']
        except KeyError: return JsonResponse({"message": "Missing required field options"}, status=400)

        order_detail['options'] = [0] * len(options)

        for j, option in enumerate(options):
            # option_idをチェック
            try:
                option = Option.objects.get(id=option['option_id'])
            except ObjectDoesNotExist:
                return JsonResponse({"message": "Option not found"}, status=400)
            if not AvailableOption.objects.filter(option_id=option, item_id=item).exists():
                return JsonResponse({"message": "Chosen option is unavailable for that item"}, status=400)
            order_detail['options'][j] = option

        order_details_objects[i] = order_detail

    # Orderレコードの作成
    order = Order(table_id=table)
    order.save()
    
    # outputを準備
    output = {
        'ordered_at': order.created_at.strftime('%Y/%m/%d %H:%M'),
        'order_details': [0] * len(order_details_objects)
    }

    # order_detailsからOrderDetailレコード、OrderedOptionレコードを作成
    for i, order_item in enumerate(order_details_objects):
        output_order_details = {}
        # OrderDetailレコードを作成
        order_detail = OrderDetail(
            item_id = order_item['item'],
            order_id = order
        )
        order_detail.save()

        options = order_item['options']
        output_order_details['options'] = [0] * len(options)

        # OrderedOptionレコードを作成
        for j, option in enumerate(options):
            OrderedOption.objects.create(
                option_id = option,
                order_detail_id = order_detail
            )
            output_order_details['options'][j] = {
                'option_id': option.id,
                'option_name': option.option_name
            }
        
        output_order_details['item'] = {
            'item_id': item.id,
            'item_name': item.item_name,
            'price': item.price
        }

        output['order_details'][i] = output_order_details

    return JsonResponse(output, status=201)

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