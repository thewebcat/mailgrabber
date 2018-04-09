from django.http import HttpResponse
from django.shortcuts import render

from mailgrabber.decorators import render_to, render_to_json
from elasticsearch import Elasticsearch, TransportError


@render_to('base.html')
def search_form(request):
    return {}


@render_to_json
def search(request):
    es = Elasticsearch()
    startswith = request.GET.get('startswith')

    body = {
        "query": {
            "bool": {"should": [
                {"simple_query_string": {
                    "query": startswith,
                    "fields": ["subject", "msg"]
                }}
            ]}
        },
        "highlight": {
            "pre_tags": ["<strong>"],
            "post_tags": ["</strong>"],
            "fields": {
                "subject": {"fragment_size": 150, "number_of_fragments": 1},
                "msg": {"fragment_size": 150, "number_of_fragments": 1}
            }
        }
    }

    items = []

    try:
        res = es.search(index='mailer', body=body)
        for hit in res['hits']['hits']:
            items.append({**hit['_source'], **hit['highlight']})
        count = res['hits']['total']
    except TransportError:
        count = 0

    return {
        "items": items,
        "query": startswith,
        "count": count,
        "empty": True if count < 1 else False,
    }
