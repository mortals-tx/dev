from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import CVE
from app.libs.success_types import Success


cve = Redprint('cve')


@cve.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    cve_id = request.args.get('cve_id', '', type=str)
    cve_name = request.args.get('cve_name', '', type=str)
    cve_type = request.args.get('cve_type', '', type=str)
    cve_status = request.args.get('cve_status', '', type=str)
    cve_time = request.args.get('cve_time', '', type=str)
    status = request.args.get('status', 1, type=int)
    cve_from = request.args.get('cve_from', '', type=str)
    created_hour = request.args.get('created_hour', 0, type=int) # 小时,即取多少小时内的数据，用于报警
    pagination = CVE.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, cve_id=cve_id,                                                    
                                                    cve_name=cve_name, cve_type=cve_type, cve_status=cve_status, 
                                                    cve_from=cve_from, status=status, created_hour=created_hour, cve_time=cve_time)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'cve_id': h.cve_id,
            'cve_url': h.cve_url,
            'cve_name': h.cve_name,
            'cve_type': h.cve_type,
            'cve_time': h.cve_time,
            'cve_status': h.cve_status,
            'status': h.status,
            'cve_from': h.cve_from,
            'utc_created': h.utc_created,
            'utc_modified': h.utc_modified
        } for h in pagination.items]
    }
    return Success(msg=data)

@cve.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    with db.auto_commit():
        h = CVE.get_item_by_uid(uid=uid)
        h.update(**data)
    return Success()


@cve.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    cve_id = data.get('cve_id')
    cve_url = data.get('cve_url')
    cve_name = data.get('cve_name')
    cve_type = data.get('cve_type')
    cve_status = data.get('cve_status')
    cve_time = data.get('cve_time')
    cve_from = data.get('cve_from')
    with db.auto_commit():
        CVE.save(cve_id=cve_id, cve_url=cve_url, cve_name=cve_name, cve_type=cve_type,cve_status=cve_status, cve_from=cve_from, cve_time=cve_time )
    return Success()


@cve.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = CVE.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        h.activate()
    return Success()


@cve.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = CVE.get_item_by_uid(uid)
    with db.auto_commit():
        h.remove()
    return Success()
