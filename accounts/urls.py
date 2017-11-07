from django.conf.urls import url

from .views import UsernameSearchFormView

urlpatterns = [
    url(
        r'^username_search_form/',
        UsernameSearchFormView.as_view(),
        name='username_search_form',
    ),
]
