# 白名单IP以及端口， 包括蜜罐IP、前置以及不可扫描IP
from app.models import BaseModel
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, CHAR

class WhiteHost(BaseModel):

    __tablename__ = 'asset_white_host'

    ip = Column(CHAR(19), nullable=False)  # IP
    port = Column(CHAR(9)) # 端口
    origin = Column(VARCHAR(64))  # 数据来源

    _fields = ['uid', 'ip', 'port', 'origin']

    def _set_fields(self):
        self._fields = ['uid', 'ip', 'port', 'origin']

    def remove(self):
        WhiteHost.query.filter(WhiteHost.uid == self.uid).delete()

    @classmethod
    def get_item_by_ip(cls, ip=None):
        query = WhiteHost.query.filter(WhiteHost.ip == ip)
        return query.first()

    @classmethod
    def get_item_by_uid(cls, uid):
        return WhiteHost.query.filter(WhiteHost.uid == uid).first()

    @classmethod
    def list_items(cls):
        return WhiteHost.query.all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None,
                                      ip=None, port=None, origin=None):
        query = WhiteHost.query
        if uid:
            query = query.filter(WhiteHost.uid == uid)
        if ip:
            query = query.filter(WhiteHost.ip.ilike('%{}%'.format(ip)))
        if port:
            query = query.filter(WhiteHost.port.ilike('%{}%'.format(port)))
        if origin:
            query = query.filter(WhiteHost.origin.ilike('%{}%'.format(origin)))
        return query.order_by(WhiteHost.utc_created.desc()).paginate(
            page=page, per_page=per_page
        )
