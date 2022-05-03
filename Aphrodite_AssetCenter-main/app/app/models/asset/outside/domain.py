from pydoc import resolve
from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import CHAR,VARCHAR, LONGTEXT
from sqlalchemy.types import JSON


class Domain(BaseModel):

    __tablename__ = 'asset_domain'

    name = Column(VARCHAR(64), nullable=False, unique=True)  # 域名
    resolve_ip = Column(LONGTEXT)  # 解析IP
    origin = Column(VARCHAR(64))  # 数据来源
    zone_uid = Column(UUID)  # zone_uid 所属区域ID

    _fields = ['uid', 'name', 'resolve_ip','origin','zone_uid']

    def _set_fields(self):
        self._fields = ['uid', 'name', 'resolve_ip','origin','zone_uid']

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid, status=1):
        return Domain.query.filter(Domain.status == status, Domain.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, 
                                      name=None, resolve_ip=None, origin=None, status=1):
        query = Domain.query
        if uid:
            query = query.filter(Domain.uid == uid)
        if status in [0, 1]:
            query = query.filter(Domain.status == status)
        if name:
            query = query.filter(Domain.name.ilike('%{}%'.format(name)))
        if resolve_ip:
            query = query.filter(Domain.resolve_ip.ilike('%{}%'.format(resolve_ip)))            
        if origin:
            query = query.filter(Domain.origin.ilike('%{}%'.format(origin)))
        return query.order_by(Domain.utc_modified.desc()).paginate(
            page=page, per_page=per_page
        )

    @classmethod
    def get_item_by_name(cls, name, status=1):
        return Domain.query.filter(Domain.status == status, Domain.name == name).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Domain.query.filter(Domain.status == status, Domain.uid == uid).first()
