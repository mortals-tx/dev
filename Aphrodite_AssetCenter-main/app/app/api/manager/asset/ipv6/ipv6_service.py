from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models.asset import Ipv6Service, Zone
from app.libs.success_types import Success


ipv6service = Redprint('ipv6service')


@ipv6service.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    zone_uid = request.args.get('zone_uid', '', type=str)
    uid = request.args.get('uid', '', type=str)
    ipv6 = request.args.get('ipv6', '', type=str)
    port = request.args.get('port', '', type=str)
    name = request.args.get('name', '', type=str)
    protocol = request.args.get('protocol', '', type=str)
    tunnel = request.args.get('tunnel', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    status = request.args.get('status', 1, type=int)
    info = request.args.get('info', '', type=str)
    utc_created = request.args.get('utc_created', '', type=str)
    pagination = Ipv6Service.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,
                                                       ipv6=ipv6, port=port, status=status, cpe=cpe, name=name,
                                                       zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                       protocol=protocol, tunnel=tunnel, info=info, utc_created=utc_created)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': s.uid,
            'zone_uid': s.zone_uid,
            'host_uid': s.host_uid,
            'ipv6': s.ipv6,
            'port': s.port,
            'protocol': s.protocol,
            'tunnel': s.tunnel,
            'name': s.name,
            'cpe': s.cpe,
            'status': s.status,
            'info': s.info,
            'utc_created': s.utc_created,
            'utc_modified': s.utc_modified            
        } for s in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)
