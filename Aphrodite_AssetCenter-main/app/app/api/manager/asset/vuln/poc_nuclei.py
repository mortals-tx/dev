from re import template
from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.libs.success_types import Success
from app.models.asset import PocVuln

pocvuln = Redprint('pocvuln')

@pocvuln.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    host = request.args.get('host', '', type=str)
    template_id = request.args.get('template_id', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = PocVuln.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, host=host,
                                                    template_id=template_id, status=status)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'host': h.host,
            'template_id': h.template_id,
            'info': h.info,
            'status': h.status,
            'utc_created': h.utc_created,
            'utc_modified': h.utc_modified
        } for h in pagination.items]
    }
    return Success(msg=data)



@pocvuln.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    host = data.get('host')
    template_id = data.get('template-id')
    info = data
    with db.auto_commit():
        PocVuln.save(host=host, template_id=template_id, info=info)
    return Success()


@pocvuln.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = PocVuln.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        h.activate()
    return Success()


@pocvuln.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = PocVuln.get_item_by_uid(uid)
    with db.auto_commit():
        h.remove()
    return Success()
