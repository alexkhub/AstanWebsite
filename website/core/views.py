from django.http import HttpResponse


def dashboard_view(request):
    # write your view processing logics here
    return HttpResponse("Welcome to Dashboard")
