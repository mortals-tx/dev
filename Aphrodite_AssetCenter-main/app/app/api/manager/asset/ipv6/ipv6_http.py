from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import Ipv6Http, Zone
from app.libs.success_types import Success
import json

ipv6http = Redprint('ipv6http')


@ipv6http.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', None, type=str)
    website = request.args.get('website', '', type=str)
    http_status = request.args.get('http_status', '', type=str)
    title = request.args.get('title', '', type=str)
    cms = request.args.get('cms', '', type=str)    
    product = request.args.get('product', '', type=str)
    status = request.args.get('status', 1, type=int)
    utc_created = request.args.get('utc_created', '', type=str)
    pagination = Ipv6Http.list_items_paginate_by_search(
        page=page_no, 
        per_page=page_size, 
        uid=uid,
        zone_list=Zone.recursion_children_uid_list(zone_uid), 
        website=website,
        http_status=http_status,
        title=title, 
        cms=cms,
        product=product,
        status=status,
        utc_created = utc_created
        )
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'zone_uid': h.zone_uid,
            'website': h.website,  
            'http_status': h.http_status,          
            'title': h.title,
            'cms' : h.cms,
            'product': h.product,  
            'status': h.status,          
            'info': h.info,
            'utc_created': h.utc_created,
            'utc_modified': h.utc_modified                  
        } for h in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)

# 管理台-修改
@ipv6http.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    website = data.get('website')
    http_status = data.get('http_status') 
    title = data.get('title')
    size = data.get('size')
    cms = data.get('cms')
    product = data.get('product')
    zone_uid = data.get('zone_uid')
    info = data.get('info')
    h = Ipv6Http.get_item_by_uid(uid=uid)
    with db.auto_commit():
        h.update(website=website, http_status=http_status, title=title, size=size, cms=cms, product=product, zone_uid=zone_uid, info=info)
    return Success()

# 管理台-新增
@ipv6http.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    website = data.get('website')
    http_status = data.get('http_status') 
    title = data.get('title')
    size = data.get('size')
    cms = data.get('cms')
    product = data.get('product')
    zone_uid = data.get('zone_uid')
    info = json.loads(data.get('info'))
    with db.auto_commit():
        Ipv6Http.save(website=website, http_status=http_status, title=title, size=size, cms=cms, product=product, zone_uid=zone_uid, info=info)
    return Success()

@ipv6http.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = Ipv6Http.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        h.activate()
    return Success()


@ipv6http.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = Ipv6Http.get_item_by_uid(uid)
    with db.auto_commit():
        h.remove()
    return Success()
