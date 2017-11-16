from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class NotFoundView(TemplateView):
    template_name = '404.html'
