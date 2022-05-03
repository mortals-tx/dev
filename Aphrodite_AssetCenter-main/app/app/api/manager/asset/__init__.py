import imp
from flask import Blueprint


from app.api.manager.asset.outside.host import host
from app.api.manager.asset.outside.domain import domain
from app.api.manager.asset.outside.service import service
from app.api.manager.asset.outside.http import http
from app.api.manager.asset.common.cgi import cgi
from app.api.manager.asset.common.zone import zone
from app.api.manager.asset.ipv6.ipv6_host import ipv6host
from app.api.manager.asset.ipv6.ipv6_service import ipv6service
from app.api.manager.asset.ipv6.ipv6_http import ipv6http
from app.api.manager.asset.inner.inner_host import innerhost
from app.api.manager.asset.inner.inner_service import innerservice
from app.api.manager.asset.inner.inner_http import innerhttp
from app.api.manager.asset.white_host.white_host import whitehost
from app.api.manager.asset.vuln.poc_nuclei import pocvuln
from app.api.manager.asset.vuln.web_xray import webvuln
from app.api.manager.asset.cve.cve import cve

def create_blueprint_asset():
    bp_asset = Blueprint('manager_asset', __name__)
    host.register(bp_asset)
    domain.register(bp_asset)
    service.register(bp_asset)
    http.register(bp_asset)
    cgi.register(bp_asset)
    zone.register(bp_asset)
    ipv6host.register(bp_asset)
    ipv6service.register(bp_asset)
    ipv6http.register(bp_asset)
    innerhost.register(bp_asset)
    innerservice.register(bp_asset)
    innerhttp.register(bp_asset)
    whitehost.register(bp_asset)
    pocvuln.register(bp_asset)
    webvuln.register(bp_asset)
    cve.register(bp_asset)

    return bp_asset
