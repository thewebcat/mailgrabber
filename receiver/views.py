from django.http import HttpResponse

from receiver.receiver import email_getter


def email_getter(request):
    result = []
    for item in email_getter():
        result.append(item)
    return HttpResponse(result)
