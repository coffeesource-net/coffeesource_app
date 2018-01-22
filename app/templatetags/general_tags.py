from steem import Steem

from django import template

from app import settings

register = template.Library()


@register.assignment_tag
def get_last_ecoinstant_entry():
    s = Steem(nodes=settings.STEEM_NODES)
    blog_entries = s.get_blog(
        account='ecoinstant',
        entry_id=0,
        limit=10,
    )

    for entry in blog_entries:
        comment = entry['comment']
        author = comment.get('author')

        if author == 'ecoinstant':
            entry_dict = {
                'title': comment.get('title'),
                'url': 'https://steemit.com/{0}/@{1}/{2}'.format(
                    comment.get('category'),
                    author,
                    comment.get('permlink'),
                ),
            }

            return entry_dict
    return None
