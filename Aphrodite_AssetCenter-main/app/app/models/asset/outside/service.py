from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, SMALLINT, CHAR
from sqlalchemy.types import JSON


class Service(BaseModel):

    __tablename__ = 'asset_service'
    host_uid = Column('host_uid', UUID, nullable=False, index=True)  # 多对一，主机
    host_ip = Column(CHAR(19), nullable=False) 
    port = Column(SMALLINT(unsigned=True), nullable=False)  # 端口
    protocol = Column(VARCHAR(36))  # 协议：TCP/UDP/HTTP
    tunnel = Column(VARCHAR(36))  # 通道：SSL
    name = Column(VARCHAR(64))  # 
    cpe = Column(VARCHAR(256))  #
    info = Column(JSON)  # status,banner,fingerprint,version,extra,product
    zone_uid = Column(UUID)  # zone_uid 所属区域ID

    _fields = ['uid', 'host_uid', 'host_ip', 'port', 'protocol', 'tunnel',
               'name', 'cpe', 'info', 'zone_uid']

    def _set_fields(self):
        self._fields = ['uid', 'host_uid', 'host_ip', 'port', 'protocol', 'tunnel',
                        'name', 'cpe', 'info', 'zone_uid']

    @classmethod
    def list_items_by_host_uid(cls, host_uid, status=1):
        return Service.query.filter(Service.status == status, Service.host_uid == host_uid).all()

    @classmethod
    def get_item_by_ip_port(cls, host_ip, port, status=1):
        return Service.query.filter(Service.status == status, Service.host_ip == host_ip, Service.port == port).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Service.query.filter(Service.status == status, Service.uid == uid).first()

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid):
        return Service.query.filter(Service.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, zone_list=None, host_ip=None, port=None,
                                      status=1, cpe=None, name=None, protocol=None, tunnel=None, info=None, utc_created=None):
        query = Service.query
        if uid:
            query = query.filter(Service.uid == uid)
        if zone_list:
            query = query.filter(Service.zone_uid.in_(zone_list))
        if status in [0, 1]:
            query = query.filter(Service.status == status)
        if host_ip:
            query = query.filter(Service.host_ip.ilike('%{}%'.format(host_ip)))
        if port:
            query = query.filter(Service.port == port)
        if name:
            query = query.filter(Service.name.ilike('%{}%'.format(name)))
        if protocol:
            query = query.filter(Service.protocol.ilike('%{}%'.format(protocol)))
        if tunnel:
            query = query.filter(Service.tunnel.ilike('%{}%'.format(tunnel)))
        if cpe:
            query = query.filter(Service.cpe.ilike('%{}%'.format(cpe)))
        if info:
            query = query.filter(Service.info.ilike('%{}%'.format(info)))
        if utc_created:
            query = query.filter(Service.utc_created.ilike('%{}%'.format(utc_created)))    
        return query.order_by(Service.utc_created.desc()).paginate(
            page=page, per_page=per_page
        )
