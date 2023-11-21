# Copyright (c) 2023, a and contributors
# For license information, please see license.txt

import frappe


def get_data(filters: dict):
    item_groups_list = frappe.get_list('Item Group', fields='name')
    item_groups_dict = {}
    for item_group in item_groups_list:
        item_group['name']
        item_groups_dict[item_group['name']] = []

    items = frappe.get_list(
        'Item', fields=['item_group', 'name', 'item_name', 'is_wooet_product', 'woocommerce_id'], filters=filters)
    for item in items:
        item_groups_dict[item['item_group']].append(item)
    arr = []
    for item_group in item_groups_dict.items():
        if len(item_group[1]) > 0:
            arr.append({'item_group': item_group[0], "indent": 0})
        for item in item_group[1]:
            item.indent = 1
            price = frappe.get_value(
                'Item Price', {'item_code': item.name}, 'price_list_rate')
            item.price = price
            item.item_group = ''
            item.item_group1 = item_group[0]
            arr.append(item)
    print(arr[1])
    return arr


def get_columns():
    return [
        {
            'fieldname': 'item_group',
            'label': 'Item Group',
            'fieldtype': 'Link',
            'options': 'Item Group',
            'width': 150
        },
        {
            'fieldname': 'name',
            'label': 'Name',
            'fieldtype': 'Link',
            'options': 'Item',
            'width': 250
        },
        {
            'fieldname': 'item_name',
            'label': 'Item Name',
            'fieldtype': 'Data',
            'options': 'Item',
            'width': 450
        },
        {
            'fieldname': 'price',
            'label': 'Price',
            'fieldtype': 'Currency',
            'options': '',
            'width': 150
        },
        {
            'fieldname': 'is_wooet_product',
            'label': 'Is Woocommerce Product',
            'fieldtype': 'Check',
            'options': 'Item',
            'width': 50
        },
        {
            'fieldname': 'woocommerce_id',
            'label': 'Woocommerce ID',
            'fieldtype': 'Data',
            'options': 'Item',
            'width': 50
        },

    ]


def get_stats(data: list):
    labels = {}
    for dic in data:

        if dic['indent'] != 0:
            labels[dic['item_group1']] += 1
        else:
            labels[dic['item_group']] = 0
    return {"keys": list(labels.keys()), "vals": list(labels.values())}


def get_chart(data: list):
    d: dict = get_stats(data)
    chart = {
        'title': "Number of woocommerce products",
        'data': {
            'labels': d['keys'],
            'datasets': [{'values': d['vals']}]
        },
        'type': 'bar',
        'height': 600,
        'colors': ['#3433FF'],
        'yMarkers': [
            {
                'label': "Threshold",
                'value': 650,
                'options': {'labelPos': 'left'}  # default: 'right'
            }
        ]


        # 'lineOptions':{'hideDots':0, 'dotSize':6, 'regionFill':1}
    }

    return chart


def get_report_summary(data: list):
    labels = get_stats(data)

    label = labels['keys']
    vals = labels['vals']
    return [{"value": vals[id], "label": val, "datatype": "Data"} for id, val in enumerate(label)]


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    data[0]
    chart = get_chart(data)
    summary = 'This is a test report for the following columns in the chart below and the following data files are available'
    report_summary = get_report_summary(data)
    # print(columns, '\n\n', data)
    return columns, data, summary,  chart, report_summary
