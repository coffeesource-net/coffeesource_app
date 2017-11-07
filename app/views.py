from steem import Steem

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        s = Steem()
        context['account_counter'] = s.get_account_count()
        return context


class NotFoundView(TemplateView):
    template_name = '404.html'
