from flask import abort, current_app
from flask_restful import Resource
from .parsers import user_post_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from webapp.models import User
import json


class AuthApi(Resource):
    def post(self):
        args = user_post_parser.parse_args()
        print(args)
        user = User.query.filter_by(username=args['username']).one()
        if user.check_password(args['password']):
            s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
            print(type(s.dumps({'id': user.id})))
            print(type(str(s.dumps({'id': user.id}))))
            return {'token':  str(s.dumps({'id': user.id}))}
        else:
            abort(401)
