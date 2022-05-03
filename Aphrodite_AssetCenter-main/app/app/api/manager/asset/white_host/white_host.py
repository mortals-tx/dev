import imp
from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import WhiteHost
from app.libs.success_types import Success
import re

whitehost = Redprint('whitehost')


@whitehost.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    port = request.args.get('port', '', type=str)
    ip = request.args.get('ip', '', type=str)
    origin = request.args.get('origin', '', type=str)
    pagination = WhiteHost.list_items_paginate_by_search(page=page_no, per_page=page_size,ip=ip, port=port,origin=origin)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'ip': h.ip,
            'port': h.port,
            'origin': h.origin,            
            'utc_created': h.utc_created,
            'utc_modified': h.utc_modified
        } for h in pagination.items]
    }
    return Success(msg=data)


@whitehost.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    if not data.get('port') or not re.match(r'[1-9]\d*',data.get('port')):
        data.update({'port':'*'})
    with db.auto_commit():
        h = WhiteHost.get_item_by_uid(uid=uid)
        h.update(**data)
    return Success()


@whitehost.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True) 
    if not data.get('port') or not re.match(r'[1-9]\d*',data.get('port')):
        data.update({'port':'*'})    
    with db.auto_commit():
        WhiteHost.save(**data)
    return Success()


@whitehost.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    with db.auto_commit():
        h = WhiteHost.get_item_by_uid(uid)
        h.remove()
    return Success()
