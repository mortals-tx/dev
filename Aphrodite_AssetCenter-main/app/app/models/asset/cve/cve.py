from app.models import BaseModel
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, CHAR
from datetime import datetime, timedelta

class CVE(BaseModel):

    __tablename__ = 'asset_cve'

    cve_id = Column(CHAR(100), nullable=False, unique=True)  # 编号
    cve_url = Column(VARCHAR(300))  # 漏洞链接
    cve_name = Column(VARCHAR(200))  # 漏洞名称
    cve_type = Column(VARCHAR(100))  # 漏洞类型
    cve_time = Column(VARCHAR(100))  # 披露时间
    cve_status = Column(VARCHAR(100))  # 漏洞状态
    cve_from = Column(VARCHAR(100))  # 来源

    _fields = ['uid', 'cve_id', 'cve_url', 'cve_name', 'cve_type', 'cve_time', 'cve_status', 'cve_from']

    def _set_fields(self):
        self._fields = ['uid', 'cve_id', 'cve_url', 'cve_name', 'cve_type', 'cve_time', 'cve_status', 'cve_from']

    def remove(self):
        super().remove()

    @classmethod
    def get_item_by_cve_id(cls, cve_id=None, status=1):
        query = CVE.query.filter(CVE.status == status, CVE.cve_id == cve_id)
        return query.first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return CVE.query.filter(CVE.status == status, CVE.uid == uid).first()

    @classmethod
    def list_items(cls, status=1):
        return CVE.query.filter(CVE.status == status).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None,
                                      cve_id=None, status=1, cve_name=None, 
                                      cve_type=None, cve_time=None,cve_status=None, created_hour=0, cve_from=None):
        query = CVE.query
        if uid:
            query = query.filter(CVE.uid == uid)
        if status in [0, 1]:
            query = query.filter(CVE.status == status)
        if cve_id:
            query = query.filter(CVE.cve_id.ilike('%{}%'.format(cve_id)))
        if cve_name:
            query = query.filter(CVE.cve_name.ilike('%{}%'.format(cve_name)))
        if cve_type:
            query = query.filter(CVE.cve_type.ilike('%{}%'.format(cve_type)))
        if cve_time:
            query = query.filter(CVE.cve_time.ilike('%{}%'.format(cve_time)))      
        if cve_status:
            query = query.filter(CVE.cve_status.ilike('%{}%'.format(cve_status)))  
        if cve_from:
            query = query.filter(CVE.cve_from.ilike('%{}%'.format(cve_from)))  
        if created_hour > 0:
            NOW = datetime.now()
            query = query.filter(CVE.utc_created >= NOW - timedelta(hours=created_hour))                           
        return query.order_by(CVE.cve_time.desc()).paginate(
            page=page, per_page=per_page
        )
