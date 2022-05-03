from app import create_app
from app.models import db
from app.models.auth import User, Role, Permission, RolePermission, UserRole


app = create_app()

# # 主要是模块更新后，需要重新注册账后, 更新权限
@app.cli.command()
def deploy():
    
    db.metadata.drop_all(db.engine, tables=[ 
        User.__table__, 
        Role.__table__, 
        Permission.__table__, 
        RolePermission,
        UserRole
    ]) 
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



if __name__ == '__main__':
    deploy()