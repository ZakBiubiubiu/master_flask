import datetime
from flask_restful import Resource, marshal_with, fields
from.parsers import comment_put_parser, comment_delete_parser
from webapp.models import User, Comment, db
from flask import abort
from .fields import PostTitle


comment_fields = {
    'id': fields.Integer,
    'text': fields.String,
    'user': fields.String(attribute='name'),
    'post_id': fields.String,
    'post_title': PostTitle
}
# 返回文章名呢？


class CommentApi(Resource):
    # 拉取所有评论
    @marshal_with(comment_fields)
    def get(self, post_id=None):
        if post_id:
            comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date.desc()).all()
        else:
            comments = Comment.query.order_by(Comment.date.desc()).all()
        return comments

# 修改评论：1 验证是否是作者 2 提供comment的id 3 提供comment的新内容
    def put(self, post_id=None):
        args = comment_put_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)
        comment = Comment.query.filter_by(name=user.username).filter_by(id=args['id']).filter_by(post_id=post_id).one()
        if not comment:
            abort(404)
        comment.text = args['text']
        comment.date = datetime.datetime.now()

        db.session.add(comment)
        db.session.commit()

        return comment.id, 201

    def delete(self, post_id=None):
        args = comment_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)
        comment = Comment.query.filter_by(name=user.username).filter_by(id=args['id']).filter_by(post_id=post_id).one()
        if not comment:
            abort(404)

        db.session.delete(comment)
        db.session.commit()

        return '', 204
