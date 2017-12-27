import json
from steem import Steem
from dateutil import parser

from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import View
from django.template.loader import render_to_string

from .data import SELFIE_CONTEST_PLAYERS
from .data import PAPAPEPPER_CONTEST_ENTRIES
from .utils import get_user_posts


s = Steem()


class UsernameSearchFormView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('cs_username_search')
        images_backlink = request.POST.get('images_backlink')

        if images_backlink:
            return redirect('accounts:images_backlink_detail', username)

        return redirect('account_detail', username)


class AccountDetailView(TemplateView):
    template_name = 'accounts/account_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')

        if username[0] == '@':
            username = username[1:]

        account_info = s.get_account(username)
        profile_image = None
        name = None
        cover_image = None

        if account_info:
            metadata = account_info.get('json_metadata')
            if metadata:
                metadata = json.loads(metadata)
                profile = metadata.get('profile')
                profile_image = profile.get('profile_image')
                name = profile.get('name')
                cover_image = profile.get('cover_image')

            account_dict = {
                'id': account_info.get('id'),
                'username': account_info.get('name'),
                'profile_image': profile_image,
                'name': name,
                'cover_image': cover_image,
                'created': parser.parse(account_info.get('created')),
                'post_count': account_info.get('post_count'),
                'voting_power': account_info.get('voting_power'),
                'curation_rewards': account_info.get('curation_rewards'),
                'posting_rewards': account_info.get('posting_rewards'),
                'reputation': account_info.get('reputation'),
            }
            return account_dict

        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_dict = self.get_object()

        username = account_dict['username']
        entries_list = get_user_posts(
            username=username,
            from_id=0,
        )

        context['account_dict'] = account_dict
        context['entries_list'] = entries_list
        context['easy_backlink'] = True

        return context


class AjaxLoadAccountPostsView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        last_entry_id = request.GET.get('last_entry_id')
        next_entry_id = int(last_entry_id) - 1

        if next_entry_id < 0:
            return JsonResponse({'action': 'pause'})

        entries_list = get_user_posts(
            username=username,
            from_id=next_entry_id,
        )

        return JsonResponse(
            {
                'action': 'load',
                'content': render_to_string(
                    'accounts/entries/_entry_list.html',
                    context={
                        'entries_list': entries_list,
                    },
                    request=self.request,
                )
            }
        )


class ImagesBacklinkView(TemplateView):
    template_name = 'accounts/images_backlink.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images_backlink'] = True

        return context


class TrainingGrounds(TemplateView):
    template_name = 'accounts/training_grounds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training_grounds'] = True

        return context


class ImagesBacklinkViewDetail(TemplateView):
    template_name = 'accounts/images_backlink_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')

        if username[0] == '@':
            username = username[1:]

        account_info = s.get_account(username)
        profile_image = None
        name = None
        cover_image = None

        if account_info:
            metadata = account_info.get('json_metadata')
            if metadata:
                metadata = json.loads(metadata)
                profile = metadata.get('profile')
                profile_image = profile.get('profile_image')
                name = profile.get('name')
                cover_image = profile.get('cover_image')

            account_dict = {
                'id': account_info.get('id'),
                'username': account_info.get('name'),
                'profile_image': profile_image,
                'name': name,
                'cover_image': cover_image,
                'created': parser.parse(account_info.get('created')),
                'post_count': account_info.get('post_count'),
                'voting_power': account_info.get('voting_power'),
                'curation_rewards': account_info.get('curation_rewards'),
                'posting_rewards': account_info.get('posting_rewards'),
                'reputation': account_info.get('reputation'),
            }
            return account_dict

        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_dict = self.get_object()

        username = account_dict['username']
        entries_list = get_user_posts(
            username=username,
            from_id=0,
        )

        context['account_dict'] = account_dict
        context['entries_list'] = entries_list
        context['images_backlink'] = True

        return context


class AjaxLoadPostsImagesView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        last_entry_id = request.GET.get('last_entry_id')
        next_entry_id = int(last_entry_id) - 1

        if next_entry_id < 0:
            return JsonResponse({'action': 'pause'})

        entries_list = get_user_posts(
            username=username,
            from_id=next_entry_id,
        )

        return JsonResponse(
            {
                'action': 'load',
                'content': render_to_string(
                    'accounts/entries/_images_backlink_list.html',
                    context={
                        'entries_list': entries_list,
                    },
                    request=self.request,
                )
            }
        )


class PepperView(TemplateView):
    template_name = 'accounts/pepper_selfie_contest.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selfie_contest'] = True
        context['selfie_contestants_list'] = SELFIE_CONTEST_PLAYERS

        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('cs_username_search')

        if username[0] == '@':
            username = username[1:]

        selfies_list = []
        registered = False

        if username in SELFIE_CONTEST_PLAYERS:
            registered = True

            s = Steem()

            for entry_dict in PAPAPEPPER_CONTEST_ENTRIES:
                selfie_dict = {
                    'title': entry_dict['title'],
                    'permlink': entry_dict['permlink'],
                    'challenge': entry_dict['challenge'],
                    'description': entry_dict['description'],
                    'prize_pool': entry_dict['prize_pool'],
                    'image': None,
                }

                entry_comments = s.get_content_replies(
                    author='papa-pepper',
                    permlink=entry_dict['permlink'],
                )

                for comment in entry_comments:
                    author = comment['author']

                    if author == username:
                        json_metadata = json.loads(comment['json_metadata'])
                        image_list = json_metadata.get('image')

                        if image_list:
                            image = image_list[0]
                            selfie_dict['image'] = image

                            break

                selfies_list.append(selfie_dict)

        return self.render_to_response(
            self.get_context_data(
                username=username,
                registered=registered,
                selfies_list=selfies_list,
            )
        )
