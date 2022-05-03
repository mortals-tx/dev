from app.models import BaseModel, UUID
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.types import JSON
from app.models.asset.common.cgi import CGI

class Http(BaseModel):

    __tablename__ = 'asset_http'
    website = Column(VARCHAR(256), nullable=False)
    http_status = Column(VARCHAR(10))
    title = Column(LONGTEXT)
    size = Column(VARCHAR(10))
    cms = Column(VARCHAR(256))
    product = Column(VARCHAR(256))
    zone_uid = Column(UUID)  # zone_uid 所属区域ID
    info = Column(JSON)  # http_status,banner,fingerprint,version,extra,product

    _fields = ['uid', 'website', 'http_status', 'title', 'size','cms', 'product', 'zone_uid', 'info']

    def _set_fields(self):
        self._fields = ['uid', 'website', 'http_status', 'title', 'size','cms', 'product', 'zone_uid', 'info']

    @property
    def cgi(self):
        return CGI.list_items_by_http_uid(http_uid=self.uid)

    @classmethod
    def get_item_by_uid(cls, uid,status=1):
        return Http.query.filter(Http.uid == uid, Http.status == status).first()

    @classmethod
    def get_item_by_website(cls, website=None):
        return Http.query.filter(Http.website == website).first()

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid):
        return Http.query.filter(Http.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, zone_list=None,
                                      website=None, http_status=None, title=None,cms=None, product=None, status=1,utc_created=None):
        query = Http.query
        if uid:
            query = query.filter(Http.uid == uid)
        if zone_list:
            query = query.filter(Http.zone_uid.in_(zone_list))
        if website:
            query = query.filter(Http.website.ilike('%{}%'.format(website)))
        if http_status :
            query = query.filter(Http.http_status.ilike('%{}%'.format(http_status)))            
        if title:
            query = query.filter(Http.title.ilike('%{}%'.format(title)))
        if cms:
            query = query.filter(Http.cms.ilike('%{}%'.format(cms)))            
        if product:
            query = query.filter(Http.product.ilike('%{}%'.format(product)))  
        if status in [0, 1]:
            query = query.filter(Http.status == status)
        if utc_created:
            query = query.filter(Http.utc_created.ilike('%{}%'.format(utc_created)))                
        return query.order_by(Http.utc_created.desc()).paginate(
            page=page, per_page=per_page
        )
