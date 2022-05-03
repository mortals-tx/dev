from re import template
from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.libs.success_types import Success
from app.models.asset import WebVuln

webvuln = Redprint('webvuln')

@webvuln.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    host = request.args.get('host', '', type=str)
    plugin = request.args.get('plugin', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = WebVuln.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, host=host, plugin=plugin,
                                                      status=status)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'host': h.host,
            'plugin': h.plugin,            
            'info': h.info,
            'status': h.status,
            'utc_created': h.utc_created,
            'utc_modified': h.utc_modified
        } for h in pagination.items]
    }
    return Success(msg=data)



@webvuln.route('', methods=['POST'])
# xray webhook接口，鉴权则无法使用。
# @auth.login_required
def save_info():
    xray_info = request.get_json(silent=True)
    print(xray_info)
    if xray_info.get('type') != 'web_vuln':
        return 'ok'
    data = xray_info.get('data')
    host = data.get('detail').get('addr')
    plugin = data.get('plugin')
    info = data
    with db.auto_commit():
        WebVuln.save(host=host, plugin=plugin, info=info)
    return Success()


@webvuln.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = WebVuln.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        h.activate()
    return Success()


@webvuln.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = WebVuln.get_item_by_uid(uid)
    with db.auto_commit():
        h.remove()
    return Success()
