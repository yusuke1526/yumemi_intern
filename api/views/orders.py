import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

from ..models import Order, OrderDetail, OrderedOption, Item, Table, Option, AvailableOption

def validate_requests(data):
    '''
    リクエストの値を検証し、不正があればJsonResponseを返す。
    正しければDBから取得したデータを返す。
    '''
    validated_requests = {}

    # tableのチェック
    try:
        table = Table.objects.get(id=data['table_id'])
    except KeyError:
        return JsonResponse({"message": "Missing required field table_id"}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Table not found"}, status=400)

    # order_detailsのチェック
    try:
        order_details = data['order_details']
    except KeyError:
        return JsonResponse({"message": "Missing required field order_details"}, status=400)

    order_details_objects = [0] * len(order_details)

    # itemのチェック
    try:
        item_ids = set([order_item['item_id'] for order_item in order_details])
    except KeyError:
        return JsonResponse({"message": "Missing required field item_id"}, status=400)
    items_queryset = Item.objects.filter(id__in=item_ids)
    if len(item_ids) != len(items_queryset):
        return JsonResponse({"message": "Item not found"}, status=400)
    # インスタンスを保持（効率化のためquerysetは極力触らない）
    item_instances = {item.id: item for item in items_queryset}

    # optionのチェック
    try:
        option_ids = []
        for order_item in order_details:
            for option in order_item['options']:
                option_ids.append(option['option_id'])
    except KeyError:
        return JsonResponse({"message": "Missing required field option_id"}, status=400)
    option_ids = set(option_ids)
    options_queryset = Option.objects.filter(id__in=option_ids)
    if len(option_ids) != len(options_queryset):
        return JsonResponse({"message": "Option not found"}, status=400)
    option_instances = {option.id: option for option in options_queryset}

    # itemとoptionの組み合わせをチェック
    # リクエストに含まれるitemを含むavailable_optionを取ってくる
    available_options_queryset = AvailableOption.objects.select_related('item_id', 'option_id').filter(item_id__in=item_ids)
    available_options_instances = \
        {(available_option.item_id, available_option.option_id): available_option for available_option in available_options_queryset}
    for order_detail in order_details:
        item_id = order_detail['item_id']
        ops = [option['option_id'] for option in order_detail['options']]
        # 取得したavailable_optionのうちorder_detailで指定されたoptionのみを取り出す。
        aops = [key[1].id for key in available_options_instances.keys() if key[0].id==item_id and key[1].id in ops]
        if len(ops) != len(aops):
            return JsonResponse({"message": "Chosen option is unavailable for that item"}, status=400)

    validated_requests['table'] = table
    validated_requests['item_instances'] = item_instances
    validated_requests['option_instances'] = option_instances
    return validated_requests

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

    # validate
    response = validate_requests(data)
    if type(response) == JsonResponse: return response
    table = response['table']
    item_instances = response['item_instances']
    option_instances = response['option_instances']
    order_details = data['order_details']

    # Orderレコードの作成
    order = Order(table_id=table)
    order.save()
    
    # outputを準備
    output = {
        'ordered_at': order.created_at.strftime('%Y/%m/%d %H:%M'),
        'order_details': [0] * len(order_details)
    }

    add_order_details = [0] * len(order_details)
    add_ordered_options = []

    # order_detailsからOrderDetailレコード、OrderedOptionレコードを作成
    for i, order_item in enumerate(order_details):
        output_order_details = {}
        # OrderDetailレコードを作成
        item = item_instances[order_item['item_id']]
        order_detail = OrderDetail(
            item_id = item,
            order_id = order
        )
        add_order_details[i] = order_detail

        output_order_details['item'] = {
            'item_id': item.id,
            'item_name': item.item_name,
            'price': item.price
        }

        option_ids = [option['option_id'] for option in order_item['options']]
        options = [option for option_id, option in option_instances.items() if option_id in option_ids]
        output_order_details['options'] = [0] * len(options)

        # OrderedOptionレコードを作成
        for j, option in enumerate(options):
            ordered_option = OrderedOption(
                option_id = option,
                order_detail_id = order_detail
            )
            add_ordered_options.append(ordered_option)
            output_order_details['options'][j] = {
                'option_id': option.id,
                'option_name': option.option_name
            }
        
        output['order_details'][i] = output_order_details

    OrderDetail.objects.bulk_create(add_order_details)
    OrderedOption.objects.bulk_create(add_ordered_options)

    return JsonResponse(output, status=201)