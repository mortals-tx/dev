from app import create_app
from werkzeug.exceptions import HTTPException
from app.libs.errors import APIException
from app.libs.error_types import ServerException
from app.models import db
from app.models.auth import User, Role, Permission, RolePermission, UserRole
from app.models.asset import Host, Service, Domain, Http, CGI, Zone


app = create_app()

# app_context_processor作为一个装饰器修饰一个函数
# dict中的key将作为变量在所有模板中可见
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role, Permission=Permission,
                RolePermission=RolePermission, UserRole=UserRole,
                Host=Host, Service=Service, Domain=Domain, Http=Http, CGI=CGI, Zone=Zone)

# app.cli.command() 创建自定义命令: flask perup
@app.cli.command()
def perup():
    with db.auto_commit():
        for item in Permission.query.all():
            db.session.delete(item)
    with db.auto_commit():
        for item in app.url_map.iter_rules():
            if item.endpoint != 'static':
                Permission.save(endpoint=item.endpoint)
        admin_role = Role.get_item_by_name(name='admin')
        admin_role.update(permissions=[permission for permission in Permission.list_items()])

# 生成相关数据库和默认数据
@app.cli.command()
def deploy():
    db.drop_all()
    db.create_all()
    # Web初始管理员用户密码
    users = [
        {
            'name': 'thinkzheng',
            'password': 'XKxREuKUcTLt2LYE'
        },
    ]
    roles = [
        {'name': 'admin'},
    ]
    with db.auto_commit():
        for user in users:
            User.save(**user)
        for role in roles:
            Role.save(**role)
        for item in app.url_map.iter_rules():
            if item.endpoint != 'static':
                Permission.save(endpoint=item.endpoint)
    with db.auto_commit():
        admin_user = User.get_item_by_name(name='thinkzheng')
        admin_role = Role.get_item_by_name(name='admin')
        admin_role.update(permissions=[permission for permission in Permission.list_items()])
        admin_user.update(roles=[admin_role])
    with db.auto_commit():
        # Zone.save(name='test')
        Zone.save(name='外网')
        Zone.save(name='内网')
        Zone.save(name='IPV6')

@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 998
        return APIException(msg, code, error_code)
    else:
        if not app.config['DEBUG']:
            return ServerException()
        else:
            return e

if __name__ == '__main__':
    # deploy()
    app.run(host='0.0.0.0',debug=True)
