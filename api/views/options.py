import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from ..models import Order, OrderDetail, OrderedOption, Item, Table, Option, AvailableOption, ItemGenre

# Create your views here.
def items_options(request, item_id):
    '''
    item_idで指定したitemで利用可能なoptionsを取得する。

    Parameter:
        int: item_id

    Response
    200 OK
    {
        "options": [
            {
                "option_id": 1,
                "option_name": "チリソース"
            }
        ]
    }
    '''

    output = {'options': []}

    item = Item.objects.get(id=item_id)
    available_options = AvailableOption.objects.select_related('option_id').filter(item_id=item)
    output = {'options': [0] * len(available_options)}
    for i, available_option in enumerate(available_options):
        option = available_option.option_id
        output['options'][i] = {'option_id': option.id, 'option_name': option.option_name}

    return JsonResponse(output, status=200)