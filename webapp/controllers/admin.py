from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from webapp.forms import CKTextAreaField
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import login_required, current_user
from webapp.exts import admin_permission


class CustomView(BaseView):
    @expose('/')
    @login_required
    @admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated() and admin_permission.can()


class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated() and admin_permission.can()


class PostView(CustomModelView):
    form_overrides = dict(text=CKTextAreaField)  # 使用新字段替换旧字段
    column_searchable_list = ('text', 'title')  # 定义哪些字段可以通过文本搜索
    column_filters = ('publish_date', )
    # column_exclude_list = ['text' ]  # 排除字段
    can_view_details = True  # 查看详情选项
    column_editable_list = ['title']
    # create_modal = True

    create_template = 'admin/model/post_edit.html'
    edit_template = 'admin/model/post_edit.html'

