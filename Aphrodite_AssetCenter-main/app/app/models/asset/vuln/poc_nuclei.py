from re import template
from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy.types import JSON


class PocVuln(BaseModel):

    __tablename__ = 'asset_poc_vuln'

    host = Column(VARCHAR(256), nullable=False)  # host
    template_id = Column(VARCHAR(256))  # poc模板
    info = Column(JSON)  # 详细信息

    _fields = ['host', 'template_id', 'info']

    def _set_fields(self):
        self._fields = ['host', 'template_id', 'info']

    def remove(self):
        super().remove()

    @classmethod
    def get_item_by_host(cls, host=None, status=1):
        query = PocVuln.query.filter(PocVuln.status == status, PocVuln.host == host)
        return query.first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return PocVuln.query.filter(PocVuln.status == status, PocVuln.uid == uid).first()

    @classmethod
    def list_items(cls, status=1):
        return PocVuln.query.filter(PocVuln.status == status).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None,
                                      host=None, status=1, template_id=None, utc_created=None):
        query = PocVuln.query
        if uid:
            query = query.filter(PocVuln.uid == uid)
        if status in [0, 1]:
            query = query.filter(PocVuln.status == status)
        if host:
            query = query.filter(PocVuln.host.ilike('%{}%'.format(host)))
        if template_id:
            query = query.filter(PocVuln.template_id.ilike('%{}%'.format(template_id)))
        if utc_created:
            query = query.filter(PocVuln.utc_created.ilike('%{}%'.format(utc_created)))    
        return query.order_by(PocVuln.utc_modified.desc()).paginate(
            page=page, per_page=per_page
        )
