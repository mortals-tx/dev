from re import template
from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy.types import JSON


class WebVuln(BaseModel):

    __tablename__ = 'asset_vuln_web'

    host = Column(VARCHAR(256), nullable=False)  # host
    plugin = Column(VARCHAR(256))  # 扫描插件
    info = Column(JSON)  # 详细信息

    _fields = ['host', 'plugin', 'info']

    def _set_fields(self):
        self._fields = ['host', 'plugin', 'info']

    def remove(self):
        super().remove()

    @classmethod
    def get_item_by_host(cls, host=None, status=1):
        query = WebVuln.query.filter(WebVuln.status == status, WebVuln.host == host)
        return query.first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return WebVuln.query.filter(WebVuln.status == status, WebVuln.uid == uid).first()

    @classmethod
    def list_items(cls, status=1):
        return WebVuln.query.filter(WebVuln.status == status).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None,
                                      host=None, plugin=plugin, status=1, utc_created=None):
        query = WebVuln.query
        if uid:
            query = query.filter(WebVuln.uid == uid)
        if status in [0, 1]:
            query = query.filter(WebVuln.status == status)
        if host:
            query = query.filter(WebVuln.host.ilike('%{}%'.format(host)))
        if plugin:
            query = query.filter(WebVuln.plugin.ilike('%{}%'.format(plugin)))            
        if utc_created:
            query = query.filter(WebVuln.utc_created.ilike('%{}%'.format(utc_created)))    
        return query.order_by(WebVuln.utc_modified.desc()).paginate(
            page=page, per_page=per_page
        )
