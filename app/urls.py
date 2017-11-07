from django.conf.urls import url
from django.conf.urls import include

from .views import HomeView
from accounts.views import AccountDetailView


urlpatterns = [

    url(
        r'^$',
        HomeView.as_view(),
        name='home',
    ),

    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    url(
        r'^(?P<username>[-\w.@]+)/$',
        AccountDetailView.as_view(),
        name='account_detail',
    ),
]
