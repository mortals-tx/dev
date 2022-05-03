from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import Ipv6Host, Zone
from app.libs.success_types import Success


ipv6host = Redprint('ipv6host')


@ipv6host.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', None, type=str)
    ipv6 = request.args.get('ipv6', '', type=str)
    origin = request.args.get('origin', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = Ipv6Host.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ipv6=ipv6,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    origin=origin, cpe=cpe, status=status)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'ipv6': h.ipv6,
            'zone_uid': h.zone_uid,
            'origin': h.origin,
            'cpe': h.cpe,
            'service_count': h.service_count,
            'status': h.status,
            'info': h.info,
            'utc_created': h.utc_created,
            'utc_modified': h.utc_modified            
        } for h in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)


@ipv6host.route('/service', methods=['GET'])
@auth.login_required
def get_service():
    uid = request.args.get('uid', '', type=str)
    h = Ipv6Host.get_item_by_uid(uid=uid)
    data = {
        'pageSize': len(h.services),
        'pageNo': 1,
        'totalCount': len(h.services),
        'data': h.services
    }
    return Success(msg=data)


@ipv6host.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    with db.auto_commit():
        h = Ipv6Host.get_item_by_uid(uid=uid)
        h.update(**data)
    return Success()


@ipv6host.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    ipv6 = data.get('ipv6')
    origin = data.get('origin')
    zone_uid = Zone.get_item_by_name("IPV6").uid
    with db.auto_commit():
        Ipv6Host.save(ipv6=ipv6, origin=origin, zone_uid=zone_uid)
    return Success()

@ipv6host.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = Ipv6Host.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        h.activate()
    return Success()

@ipv6host.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = Ipv6Host.get_item_by_uid(uid)
    with db.auto_commit():
        h.remove()
    return Success()
