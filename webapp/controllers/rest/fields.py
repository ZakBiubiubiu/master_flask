from HTMLParser import HTMLParser
from flask_restful import fields
from flask_login import current_user
from webapp.models import Post


class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
        s = HTMLStripper()
        s.feed(html)
        return s.get_data()


class HTMLField(fields.Raw):
    def format(self, value):
        return strip_tags(str(value))


class PostTitle(fields.Raw):
    def output(self, key, obj):
        return Post.query.filter_by(id=obj.post_id).one().title
