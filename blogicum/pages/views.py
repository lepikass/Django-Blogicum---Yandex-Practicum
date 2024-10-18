# pages/views.py
from django.views import View
from django.shortcuts import render


class AboutView(View):
    def get(self, request):
        return render(request, 'pages/about.html')


class RulesView(View):
    def get(self, request):
        return render(request, 'pages/rules.html')


class CsrfFailureView(View):
    def get(self, request, reason=''):
        return render(request, 'pages/403csrf.html', status=403)


class PageNotFoundView(View):
    def get(self, request, exception):
        return render(request, 'pages/404.html', status=404)


class ServerErrorView(View):
    def get(self, request):
        return render(request, 'pages/500.html', status=500)
