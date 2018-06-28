import os

env = os.environ.get('WEBAPP_ENV','dev')
print(env)
print('webapp.config.%sConfig' % env.capitalize())