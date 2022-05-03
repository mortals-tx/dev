from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, SMALLINT, CHAR
from sqlalchemy.types import JSON


class InnerService(BaseModel):

    __tablename__ = 'asset_inner_service'
    host_uid = Column('host_uid', UUID, nullable=False, index=True)  # 多对一，主机
    host_ip = Column(CHAR(19), nullable=False) 
    port = Column(SMALLINT(unsigned=True), nullable=False)  # 端口
    protocol = Column(VARCHAR(36))  # 协议：TCP/UDP/HTTP
    tunnel = Column(VARCHAR(36))  # 通道：SSL
    name = Column(VARCHAR(64))  # SSL
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
        return InnerService.query.filter(InnerService.status == status, InnerService.host_uid == host_uid).all()

    @classmethod
    def get_item_by_ip_port(cls, host_ip, port, status=1):
        return InnerService.query.filter(InnerService.status == status, InnerService.host_ip == host_ip, InnerService.port == port).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return InnerService.query.filter(InnerService.status == status, InnerService.uid == uid).first()

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid):
        return InnerService.query.filter(InnerService.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, zone_list=None, host_ip=None, port=None,
                                      status=1, cpe=None, name=None, protocol=None, tunnel=None, info=None, utc_created=None):
        query = InnerService.query
        if uid:
            query = query.filter(InnerService.uid == uid)
        if zone_list:
            query = query.filter(InnerService.zone_uid.in_(zone_list))
        if status in [0, 1]:
            query = query.filter(InnerService.status == status)
        if host_ip:
            query = query.filter(InnerService.host_ip.ilike('%{}%'.format(host_ip)))
        if port:
            query = query.filter(InnerService.port == port)
        if name:
            query = query.filter(InnerService.name.ilike('%{}%'.format(name)))
        if protocol:
            query = query.filter(InnerService.protocol.ilike('%{}%'.format(protocol)))
        if tunnel:
            query = query.filter(InnerService.tunnel.ilike('%{}%'.format(tunnel)))
        if cpe:
            query = query.filter(InnerService.cpe.ilike('%{}%'.format(cpe)))
        if info:
            query = query.filter(InnerService.info.ilike('%{}%'.format(info)))
        if utc_created:
            query = query.filter(InnerService.utc_created.ilike('%{}%'.format(utc_created)))                         
        return query.order_by(InnerService.utc_created.desc()).paginate(
            page=page, per_page=per_page
        )
