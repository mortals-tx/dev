from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, SMALLINT, CHAR
from sqlalchemy.types import JSON


class Ipv6Service(BaseModel):

    __tablename__ = 'asset_ipv6_service'
    host_uid = Column('host_uid', UUID, nullable=False, index=True)  # 多对一，主机
    ipv6 = Column(CHAR(100), nullable=False) 
    port = Column(SMALLINT(unsigned=True), nullable=False)  # 端口
    protocol = Column(VARCHAR(36))  # 协议：TCP/UDP/HTTP
    tunnel = Column(VARCHAR(36))  # 通道：SSL
    name = Column(VARCHAR(64))  # SSL
    cpe = Column(VARCHAR(256))  #
    info = Column(JSON)  # status,banner,fingerprint,version,extra,product
    zone_uid = Column(UUID)  # zone_uid 所属区域ID

    _fields = ['uid', 'host_uid', 'ipv6', 'port', 'protocol', 'tunnel',
               'name', 'cpe', 'info', 'zone_uid']

    def _set_fields(self):
        self._fields = ['uid', 'host_uid', 'ipv6', 'port', 'protocol', 'tunnel',
                        'name', 'cpe', 'info', 'zone_uid']

    @classmethod
    def list_items_by_host_uid(cls, host_uid, status=1):
        return Ipv6Service.query.filter(Ipv6Service.status == status, Ipv6Service.host_uid == host_uid).all()

    @classmethod
    def get_item_by_ip_port(cls, ipv6, port, status=1):
        return Ipv6Service.query.filter(Ipv6Service.status == status, Ipv6Service.ipv6 == ipv6, Ipv6Service.port == port).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Ipv6Service.query.filter(Ipv6Service.status == status, Ipv6Service.uid == uid).first()

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid):
        return Ipv6Service.query.filter(Ipv6Service.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, zone_list=None, ipv6=None, port=None,
                                      status=1, cpe=None, name=None, protocol=None, tunnel=None, info=None, utc_created=None):
        query = Ipv6Service.query
        if uid:
            query = query.filter(Ipv6Service.uid == uid)
        if zone_list:
            query = query.filter(Ipv6Service.zone_uid.in_(zone_list))
        if status in [0, 1]:
            query = query.filter(Ipv6Service.status == status)
        if ipv6:
            query = query.filter(Ipv6Service.ipv6.ilike('%{}%'.format(ipv6)))
        if port:
            query = query.filter(Ipv6Service.port == port)
        if name:
            query = query.filter(Ipv6Service.name.ilike('%{}%'.format(name)))
        if protocol:
            query = query.filter(Ipv6Service.protocol.ilike('%{}%'.format(protocol)))
        if tunnel:
            query = query.filter(Ipv6Service.tunnel.ilike('%{}%'.format(tunnel)))
        if cpe:
            query = query.filter(Ipv6Service.cpe.ilike('%{}%'.format(cpe)))
        if info:
            query = query.filter(Ipv6Service.info.ilike('%{}%'.format(info))) 
        if utc_created:
            query = query.filter(Ipv6Service.utc_created.ilike('%{}%'.format(utc_created)))                                
        return query.order_by(Ipv6Service.utc_created.desc()).paginate(
            page=page, per_page=per_page
        )
