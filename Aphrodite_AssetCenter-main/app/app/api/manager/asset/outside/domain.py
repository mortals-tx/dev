from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import Domain, Zone
from app.libs.success_types import Success
import json


domain = Redprint('domain')


@domain.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    name = request.args.get('name', '', type=str)
    resolve_ip = request.args.get('resolve_ip',type=str)
    origin = request.args.get('origin', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = Domain.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,                                                      
                                                      name=name,resolve_ip=resolve_ip, origin=origin, status=status)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': d.uid,
            'name': d.name,
            'resolve_ip': d.resolve_ip,
            'origin': d.origin, 
            'status': d.status,
            'utc_created': d.utc_created,
            'utc_modified': d.utc_modified            
        } for d in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)


@domain.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    with db.auto_commit():
        d = Domain.get_item_by_uid(uid=uid)
        d.update(**data)
    return Success()


@domain.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    name = data.get('name')
    resolve_ip = data.get('resolve_ip')
    origin = data.get('origin')

    zone_uid = Zone.get_item_by_name("外网").uid
    with db.auto_commit():
        Domain.save(origin=origin, name=name, resolve_ip=resolve_ip, zone_uid=zone_uid)
    return Success()


@domain.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    d = Domain.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        d.activate()
    return Success()


@domain.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    d = Domain.get_item_by_uid(uid)
    with db.auto_commit():
        d.remove()
    return Success()
