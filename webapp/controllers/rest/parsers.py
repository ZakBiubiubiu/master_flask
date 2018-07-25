from flask_restful import reqparse

post_get_parser = reqparse.RequestParser()
# 添加一个page参数,指定返回第几页
post_get_parser.add_argument(
    'page',
    type=int,
    location=['json','args', 'headers'],
    required=False
)
# 添加一个user参数
post_get_parser.add_argument(
    'user',
    type=str,
    location=['json', 'args', 'headers']
)


# 解析器，接收标题/正文/标签列表
post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help='Title is required'
)
post_post_parser.add_argument(
    'text',
    type=str,
    required=True,
    help='Body text is required'
)
post_post_parser.add_argument(
    'tags',
    type=str,
    required=True,
    action='append'
    )
post_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to create posts'
    )

# 解析器，用来解析用户凭证信息
user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)

post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to edit posts'
)
post_put_parser.add_argument(
    'title',
    type=str,
)
post_put_parser.add_argument(
    'text',
    type=str,
)
post_put_parser.add_argument(
    'tags',
    type=str,
    action='append'
)
post_delete_parser = reqparse.RequestParser()
post_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to edit posts'
)

comment_put_parser = reqparse.RequestParser()
comment_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to get comments')
comment_put_parser.add_argument(
    'text',
    type=str,
    required=True,
    help='You got to provide the new comment')
comment_put_parser.add_argument(
    'id',
    type=int,
    required=True,
    help='which comment do you want to edit')
comment_delete_parser = reqparse.RequestParser()
comment_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to get comments')
comment_delete_parser.add_argument(
    'id',
    type=int,
    required=True,
    help='which comment do you want to delete')

