import json
from steem import Steem
from dateutil import parser
from datetime import datetime

from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import View


s = Steem()


class AccountDetailView(TemplateView):
    template_name = 'accounts/account_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')

        if username[0] == '@':
            username = username[1:]

        account_info = s.get_account(username)

        location = None
        website = None
        about = None
        profile_image = None
        name = None
        cover_image = None

        if account_info:
            metadata = account_info.get('json_metadata')
            if metadata:
                metadata = json.loads(metadata)
                profile = metadata.get('profile')
                location = profile.get('location')
                website = profile.get('website')
                about = profile.get('about')
                profile_image = profile.get('profile_image')
                name = profile.get('name')
                cover_image = profile.get('cover_image')

            account_dict = {
                'id': account_info.get('id'),
                'username': account_info.get('name'),
                'location': location,
                'website': website,
                'about': about,
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

        blog_entries = s.get_blog(
            account=account_dict['username'],
            entry_id=0,
            limit=20,
        )

        entries_list = []

        for entry in blog_entries:
            comment = entry['comment']
            metadata = json.loads(comment.get('json_metadata'))

            # Could be util to load posts on utopian directly.
            # parent_permlink = comment.get('permlink')
            author = comment.get('author')
            category = comment.get('category')

            now = datetime.now()

            last_payout = parser.parse(comment.get('last_payout'))
            cashout_time = parser.parse(comment.get('cashout_time'))

            if cashout_time > now:
                last_payout = None
            else:
                cashout_time = None

            entry_dict = {
                'id': comment.get('id'),
                'title': comment.get('title'),
                'url': 'https://steemit.com/{0}/@{1}/{2}'.format(
                    category,
                    author,
                    comment.get('permlink'),
                ),
                'author': author,
                'category': category,
                'created': comment.get('created'),
                'active': comment.get('active'),
                'last_update': comment.get('last_update'),
                'net_votes': comment.get('net_votes'),
                'total_payout_value': comment.get('total_payout_value'),
                'curator_payout_value': comment.get('curator_payout_value'),
                'author_rewards': comment.get('author_rewards'),
                'last_payout': last_payout,
                'cashout_time': cashout_time,
                'tags': metadata.get('tags'),
                'images': metadata.get('image'),
                'links': metadata.get('links'),
                'app': metadata.get('app'),
            }

            if username == author:
                entries_list.append(entry_dict)

        context['account_dict'] = account_dict
        context['entries_list'] = entries_list

        return context


class UsernameSearchFormView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('cs_username_search')
        print(username)

        return redirect('account_detail', username)
