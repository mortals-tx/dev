from flask import request
from app.libs.redprint import Redprint
from app.libs.auth import auth
from app.libs.success_types import Success, NotContent
from app.models.asset import Zone, CGI, Domain, Host, Service, Http, Ipv6Host, Ipv6Service, Ipv6Http, InnerHost, InnerService, InnerHttp, WhiteHost
from app.models import db
import re

asset = Redprint('asset')

####### 外网API #######
# 外网IP API
@asset.route('/host', methods=['GET'])
@auth.login_required
def get_host():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    ip = request.args.get('ip', '', type=str)
    origin = request.args.get('origin', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = Host.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ip=ip,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    origin=origin, cpe=cpe, status=1)
    return Success(msg=pagination)

@asset.route('/host/batch', methods=['POST'])
@auth.login_required
def host_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                host = Host.query.filter(Host.ip == info.get('ip')).first()
                if host:
                    host.activate()
                    host.update(**info)
                else:
                    info['zone_uid'] = Zone.get_item_by_name('外网').uid
                    Host.save(**info)
    elif action == 'delete':
        with db.auto_commit():
            for ip in info_list:
                host = Host.get_item_by_ip(ip)
                host.remove()
    return NotContent()

# 外网域名 API
@asset.route('/domain', methods=['GET'])
@auth.login_required
def get_domain():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)    
    name = request.args.get('name', '', type=str)
    resolve_ip = request.args.get('resolve_ip', '', type=str)
    origin = request.args.get('origin', '', type=str)
    pagination = Domain.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,                                                      
                                                      name=name,resolve_ip=resolve_ip, origin=origin, status=1)
    return Success(msg=pagination)

@asset.route('/domain/batch', methods=['POST'])
@auth.login_required
def domain_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                domain = Domain.query.filter(Domain.name == info.get('name')).first()
                if domain:
                    domain.activate()
                    domain.update(**info)
                else:
                    Domain.save(**info)
    elif action == 'delete':
        with db.auto_commit():
            for name in info_list:
                domain = Domain.get_item_by_name(name)
                domain.remove()
    return NotContent()

# 外网服务 API
@asset.route('/service', methods=['GET'])
@auth.login_required
def get_service():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    host_ip = request.args.get('host_ip', '', type=str)
    port = request.args.get('port', '', type=str)
    name = request.args.get('name', '', type=str)
    protocol = request.args.get('protocol', '', type=str)
    tunnel = request.args.get('tunnel', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = Service.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, host_ip=host_ip,
                                                       port=port, status=1, cpe=cpe, name=name,
                                                       zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                       protocol=protocol, tunnel=tunnel)
    return Success(msg=pagination)

@asset.route('/service/batch', methods=['POST'])
@auth.login_required
def service_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                # 这里判断host_ip及对应端口是否已存在，存在则修改，不存在则新增                
                service = Service.query.filter(Service.host_ip == info.get('host_ip'), Service.port == info.get('port')).first()                
                if service:
                    service.update(**info)
                else:
                    # 判断hostip 是否在IP资产列表，没有则新增加入
                    if not Host.get_item_by_ip(info.get('host_ip')):
                        new_host_info = {
                            "ip": info.get('host_ip'),
                            "origin": "service_scan",
                            "info": "",
                            'zone_uid': Zone.get_item_by_name('外网').uid
                        }
                        Host.save(**new_host_info)  
                    host_info = Host.get_item_by_ip(info.get('host_ip'))
                    info['host_uid'] = host_info.uid
                    info['zone_uid'] = host_info.zone_uid                                   
                    Service.save(**info) # 只有是新增的端口重新入库，根据时间utc_created判断为新增
                    # 更新Host的service_count字段
                    host_info.service_count = host_info.service_count + 1
                    Host.update(host_info)

    elif action == 'delete':
        with db.auto_commit():
            for uid in info_list:
                # 根据uid进行修改
                service = Service.get_item_by_uid(uid)
                service.remove()
    return NotContent()

# 外网Http API
@asset.route('/http', methods=['GET'])
@auth.login_required
def get_http():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    website = request.args.get('website', '', type=str)
    http_status = request.args.get('http_status', '', type=str)
    title = request.args.get('title', '', type=str)
    cms = request.args.get('cms', '', type=str)
    product = request.args.get('product', '', type=str)
    utc_created = request.args.get('utc_created','', type=str)
    pagination = Http.list_items_paginate_by_search(
        page=page_no, per_page=page_size, uid=uid,
        zone_list=Zone.recursion_children_uid_list(zone_uid), 
        website=website,
        http_status=http_status,
        title=title, 
        cms=cms,
        product=product,
        utc_created=utc_created
    )
    return Success(msg=pagination)

@asset.route('/http/batch', methods=['POST'])
@auth.login_required
def http_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                # 这里判断website是否已存在，不存在则新增
                http = Http.query.filter(Http.website == info.get('website')).first()
                if http:
                    http.activate()
                    http.update(**info)
                else:                 
                    Http.save(**info) # 只有是新增的website重新入库，根据时间utc_created判断为新增
    elif action == 'delete':
        with db.auto_commit():
            for website in info_list:
                http = Http.get_item_by_website(website)
                http.remove()
    return NotContent()


####### Ipv6 API #######
# Ipv6 API
@asset.route('/ipv6host', methods=['GET'])
@auth.login_required
def get_ipv6host():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    ipv6host = request.args.get('ipv6', '', type=str)
    origin = request.args.get('origin', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = Ipv6Host.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ipv6=ipv6host,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    origin=origin, cpe=cpe, status=1)
    return Success(msg=pagination)

@asset.route('/ipv6host/batch', methods=['POST'])
@auth.login_required
def ipv6host_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                ipv6host = Ipv6Host.query.filter(Ipv6Host.ipv6 == info.get('ipv6')).first()
                if ipv6host:
                    ipv6host.activate()
                    ipv6host.update(**info)
                else:
                    info['zone_uid'] = Zone.get_item_by_name('IPV6').uid
                    Ipv6Host.save(**info)
    elif action == 'delete':
        with db.auto_commit():
            for ip in info_list:
                ipv6host = Ipv6Host.get_item_by_ip(ip)
                ipv6host.remove()
    return NotContent()

# Ipv6服务 API
@asset.route('/ipv6service', methods=['GET'])
@auth.login_required
def get_ipv6service():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    ipv6 = request.args.get('ipv6', '', type=str)
    port = request.args.get('port', '', type=str)
    name = request.args.get('name', '', type=str)
    protocol = request.args.get('protocol', '', type=str)
    tunnel = request.args.get('tunnel', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = Ipv6Service.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ipv6=ipv6,
                                                       port=port, status=1, cpe=cpe, name=name,
                                                       zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                       protocol=protocol, tunnel=tunnel)
    return Success(msg=pagination)

@asset.route('/ipv6service/batch', methods=['POST'])
@auth.login_required
def ipv6service_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                # 这里判断host_ip及对应端口是否已存在，不存在则新增
                service = Ipv6Service.query.filter(Ipv6Service.ipv6 == info.get('ipv6'), Ipv6Service.port == info.get('port')).first()
                if service:
                    service.update(**info)
                else:    
                    # 判断ipv6 是否在IP资产列表，没有则新增加入
                    if not Ipv6Host.get_item_by_ip(info.get('ipv6')):
                        new_host_info = {
                            "ipv6": info.get('ipv6'),
                            "origin": "service_scan",
                            "info": "",
                            'zone_uid': Zone.get_item_by_name('IPV6').uid
                        }
                        Ipv6Host.save(**new_host_info)  
                    host_info = Ipv6Host.get_item_by_ip(info.get('ipv6'))
                    info['host_uid'] = host_info.uid
                    info['zone_uid'] = host_info.zone_uid                                       
                    Ipv6Service.save(**info) # 只有是新增的端口重新入库，根据时间utc_created判断为新增
                    # 更新Host的service_count字段
                    host_info.service_count = host_info.service_count + 1
                    Ipv6Host.update(host_info)

    elif action == 'delete':
        with db.auto_commit():
            for uid in info_list:
                # 根据uid进行修改
                service = Ipv6Service.get_item_by_uid(uid)
                service.remove()
    return NotContent()

# Ipv6 Http API
@asset.route('/ipv6http', methods=['GET'])
@auth.login_required
def get_ipv6http():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    website = request.args.get('website', '', type=str)
    http_status = request.args.get('http_status', '', type=str)
    title = request.args.get('title', '', type=str)
    cms = request.args.get('cms', '', type=str)
    product = request.args.get('product', '', type=str)
    utc_created = request.args.get('utc_created','', type=str)
    pagination = Ipv6Http.list_items_paginate_by_search(
        page=page_no, per_page=page_size, uid=uid,
        zone_list=Zone.recursion_children_uid_list(zone_uid), 
        website=website,
        http_status=http_status,
        title=title, 
        cms=cms,
        product=product,
        utc_created=utc_created
    )
    return Success(msg=pagination)

@asset.route('/ipv6http/batch', methods=['POST'])
@auth.login_required
def ipv6http_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                # 这里判断website是否已存在，不存在则新增
                http = Ipv6Http.query.filter(Ipv6Http.website == info.get('website')).first()
                if not http:                                        
                    Ipv6Http.save(**info) # 只有是新增的website重新入库，根据时间utc_created判断为新增
    elif action == 'delete':
        with db.auto_commit():
            for website in info_list:
                http = Ipv6Http.get_item_by_website(website)
                http.remove()
    return NotContent()


####### 内网 API #######
# 内网IP API
@asset.route('/innerhost', methods=['GET'])
@auth.login_required
def get_innerhost():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    ip = request.args.get('ip', '', type=str)
    origin = request.args.get('origin', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = InnerHost.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ip=ip,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    origin=origin, cpe=cpe, status=1)
    return Success(msg=pagination)

@asset.route('/innerhost/batch', methods=['POST'])
@auth.login_required
def innerhost_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                innerhost = InnerHost.query.filter(InnerHost.ip == info.get('ip')).first()
                if innerhost:
                    innerhost.activate()
                    innerhost.update(**info)
                else:
                    info['zone_uid'] = Zone.get_item_by_name('内网').uid
                    InnerHost.save(**info)
    elif action == 'delete':
        with db.auto_commit():
            for ip in info_list:
                innerhost = InnerHost.get_item_by_ip(ip)
                innerhost.remove()
    return NotContent()

# 内网服务 API
@asset.route('/innerservice', methods=['GET'])
@auth.login_required
def get_innerservice():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    zone_uid = request.args.get('zone_uid', '', type=str)
    host_ip = request.args.get('host_ip', '', type=str)
    uid = request.args.get('uid', '', type=str)
    port = request.args.get('port', '', type=str)
    name = request.args.get('name', '', type=str)
    protocol = request.args.get('protocol', '', type=str)
    tunnel = request.args.get('tunnel', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = InnerService.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, host_ip=host_ip,
                                                       port=port, status=1, cpe=cpe, name=name,
                                                       zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                       protocol=protocol, tunnel=tunnel)
    return Success(msg=pagination)

@asset.route('/innerservice/batch', methods=['POST'])
@auth.login_required
def innerservice_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                # 这里判断host_ip及对应端口是否已存在，不存在则新增
                service = InnerService.query.filter(InnerService.host_ip == info.get('host_ip'), InnerService.port == info.get('port')).first()
                if service:
                    service.update(**info)
                else:
                    # 判断hostip 是否在IP资产列表，没有则新增加入
                    if not InnerHost.get_item_by_ip(info.get('host_ip')):
                        new_innerhost_info = {
                            "ip": info.get('host_ip'),
                            "origin": "service_scan",
                            "info": "",
                            'zone_uid': Zone.get_item_by_name('内网').uid
                        }
                        InnerHost.save(**new_innerhost_info)  
                    host_info = InnerHost.get_item_by_ip(info.get('host_ip'))
                    info['host_uid'] = host_info.uid
                    info['zone_uid'] = host_info.zone_uid
                    InnerService.save(**info) # 只有是新增的端口重新入库，根据时间utc_created判断为新增
                    # 更新Host的service_count字段
                    host_info.service_count = host_info.service_count + 1
                    InnerHost.update(host_info)

    elif action == 'delete':
        with db.auto_commit():
            for uid in info_list:
                # 根据uid进行修改
                service = InnerService.get_item_by_uid(uid)
                service.remove()
    return NotContent()

# 内网 Http API
@asset.route('/innerhttp', methods=['GET'])
@auth.login_required
def get_innerhttp():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    website = request.args.get('website', '', type=str)
    http_status = request.args.get('http_status', '', type=str)
    title = request.args.get('title', '', type=str)
    cms = request.args.get('cms', '', type=str)
    product = request.args.get('product', '', type=str)
    utc_created = request.args.get('utc_created','', type=str)
    pagination = InnerHttp.list_items_paginate_by_search(
        page=page_no, per_page=page_size, uid=uid,
        zone_list=Zone.recursion_children_uid_list(zone_uid), 
        website=website,
        http_status=http_status,
        title=title, 
        cms=cms,
        product=product,
        utc_created=utc_created
    )
    return Success(msg=pagination)

@asset.route('/innerhttp/batch', methods=['POST'])
@auth.login_required
def innerhttp_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                # 这里判断website是否已存在，不存在则新增
                http = Ipv6Http.query.filter(Ipv6Http.website == info.get('website')).first()
                if not http:                                        
                    Ipv6Http.save(**info) # 只有是新增的website重新入库，根据时间utc_created判断为新增
    elif action == 'delete':
        with db.auto_commit():
            for website in info_list:
                http = Ipv6Http.get_item_by_website(website)
                http.remove()
    return NotContent()


####### 白名单IP及端口 #######
# 获取
@asset.route('/whitehost', methods=['GET'])
@auth.login_required
def get_whitehost():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    ip = request.args.get('ip', '', type=str)
    port = request.args.get('port', '', type=str)
    origin = request.args.get('origin', '', type=str)
    pagination = WhiteHost.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ip=ip, port=port, 
                                                    origin=origin)
    return Success(msg=pagination)

# 添加 & 删除
@asset.route('/whitehost/batch', methods=['POST'])
@auth.login_required
def whitehost_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                if not info.get('port') or not re.match(r'[1-9]\d*',info.get('port')):
                    info.update({'port':'*'})                
                # 这里判断website是否已存在，不存在则新增
                host = WhiteHost.query.filter(WhiteHost.ip == info.get('ip'), WhiteHost.port == info.get('port')).first()
                if not host:                                       
                    WhiteHost.save(**info) # 只有是新增的website重新入库，根据时间utc_created判断为新增
    elif action == 'delete':
        with db.auto_commit():
            for ip in info_list:
                host = WhiteHost.get_item_by_ip(ip)
                host.remove()
    return NotContent()

####### CGI API #######
# CGI API
@asset.route('/cgi', methods=['GET'])
@auth.login_required
def get_cgi():
    page_no = request.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    http_uid = request.args.get('http_uid', '', type=str)
    url = request.args.get('url', '', type=str)
    method = request.args.get('method', '', type=str)
    code = request.args.get('code', 200, type=int)
    pagination = CGI.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,
                                                   http_uid=http_uid, url=url, method=method, code=code)
    return Success(msg=pagination)

####### 用于接收nuclei poc扫描结果
####### 用于接收xray web漏洞扫描结果