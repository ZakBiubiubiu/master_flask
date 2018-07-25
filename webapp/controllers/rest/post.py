from flask_restful import Resource, fields, marshal_with
from .fields import HTMLField
from flask import abort
from webapp.models import Post, User, db, Tag
from .parsers import post_get_parser, post_post_parser, post_put_parser, post_delete_parser
import datetime

nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}
post_fields = {
    'author': fields.String(attribute=lambda x: x.author.username),
    'title': fields.String(),
    'text': HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_date': fields.DateTime(dt_format='iso8601')
}


class PostApi(Resource):
    # Resource是Methodview的子类

    @marshal_with(post_fields)
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            return post
        else:
            args = post_get_parser.parse_args()
            page = args['page'] or 1
            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)
                posts = user.posts.order_by(Post.publish_date.desc()).paginate(page, 30)
            else:
                posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 30)

            return posts.items

    def post(self, post_id=None):
        if post_id:  # 为啥要设置这条件？
            abort(400)
        else:
            args = post_post_parser.parse_args(strict=True)  # ?
            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)
            new_post = Post(args['title'], args['text'])  # 新建post对象
            new_post.date = datetime.datetime.now()
            new_post.author = user

            if args['tags']:
                for item in args['tags']:
                    tag = Tag.query.filter_by(title=item).first()
                    if tag:  # 如果数据库已经存在该tag，那就直接添加到新post中
                        new_post.tags.append(tag)
                    else:  # 不然要新建了再添加
                        new_tag = Tag(item)
                        new_post.tags.append(new_tag)

        db.session.add(new_post)
        db.session.commit()
        return new_post.id, 201

    def put(self, post_id=None):
        if not post_id:
            abort(400)
        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_put_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)
        if user != post.author:
            abort(403)

        if args['title']:
            post.title = args['title']

        if args['text']:
            post.text = args['text']

        if args['tags']:
            for item in args['tags']:
                tag = Tag.query.filter_by(title=item).first()

                if tag:
                    post.tags.append(tag)
                else:
                    new_tag = Tag(item)
                    post.tages.append(new_tag)
        db.session.add(post)
        db.session.commit()
        return post.id, 201

    def delete(self, post_id=None):
        if not post_id:
            abort(400)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if user !=post.author:
            abort(403)

        db.session.delete(post)
        db.session.commit()
        return '', 204

