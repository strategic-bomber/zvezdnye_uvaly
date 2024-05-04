import json

from django.http import JsonResponse, HttpResponse


def UnicodeJsonResponse(x, **kwargs):
    kwargs["json_dumps_params"] = kwargs.pop("json_dumps_params", {})
    kwargs["json_dumps_params"]["ensure_ascii"] = False
    kwargs["json_dumps_params"]["indent"] = 2
    return JsonResponse(x, **kwargs)


def get_body(request):
    data = request.body
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    # print('Body:', data[:100])
    data = json.loads(data or "{}")
    return data





def render_frontend(request):
    index_file = open("../frontend/dist/index.html").read()
    return HttpResponse(index_file)