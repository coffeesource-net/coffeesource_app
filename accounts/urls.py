from django.conf.urls import url

from .views import UsernameSearchFormView
from .views import AjaxLoadAccountPostsView
from .views import PepperView

urlpatterns = [
    url(
        r'^username_search_form/',
        UsernameSearchFormView.as_view(),
        name='username_search_form',
    ),

    url(
        r'^ax_load_account_posts/',
        AjaxLoadAccountPostsView.as_view(),
        name='ax_load_account_posts',
    ),

    url(
        r'^papa-pepper-selfie-contest-1/',
        PepperView.as_view(),
        name='pepper_selfie_contest',
    ),
]
