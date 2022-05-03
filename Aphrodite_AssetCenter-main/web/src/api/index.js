const api = {
  // auth.login
  getToken: '/login/token',
  getUserInfo: '/login/user_info',

  // auth.permission
  getPermissionList: '/permission',
  activatePermission: '/permission/activate',
  removePermission: '/permission/remove',

  // auth.role
  getRoleList: '/role',
  updateRoleInfo: '/role/info',
  saveRoleInfo: '/role',
  activateRole: '/role/activate',
  removeRole: '/role/remove',

  // auth.user
  getUserList: '/user',
  updateUserInfo: '/user/info',
  saveUserInfo: '/user',
  activateUser: '/user/activate',
  removeUser: '/user/remove',

  // asset.host
  getHostList: '/host',
  getHostService: '/host/service',
  updateHostInfo: '/host/info',
  saveHostInfo: '/host',
  activateHost: '/host/activate',
  removeHost: '/host/remove',

  // asset.innerhost
  getInnerHostList: '/innerhost',
  getInnerHostService: '/innerhost/service',
  updateInnerHostInfo: '/innerhost/info',
  saveInnerHostInfo: '/innerhost',
  activateInnerHost: '/innerhost/activate',
  removeInnerHost: '/innerhost/remove',

  // asset.ipv6host
  getIpv6HostList: '/ipv6host',
  getIpv6HostService: '/ipv6host/service',
  updateIpv6HostInfo: '/ipv6host/info',
  saveIpv6HostInfo: '/ipv6host',
  activateIpv6Host: '/ipv6host/activate',
  removeIpv6Host: '/ipv6host/remove',

  // asset.domain
  getDomainList: '/domain',
  updateDomainInfo: '/domain/info',
  saveDomainInfo: '/domain',
  activateDomain: '/domain/activate',
  removeDomain: '/domain/remove',

  // asset.service
  getServiceList: '/service',

  // asset.innerservice
  getInnerServiceList: '/innerservice',

  // asset.ipv6service
  getIpv6ServiceList: '/ipv6service',

  // asset.http
  getHttpList: '/http',
  updateHttpInfo: '/http/info',
  saveHttpInfo: '/http',
  activateHttp: '/http/activate',
  removeHttp: '/http/remove',

  // asset.innerhttp
  getInnerHttpList: '/innerhttp',
  updateInnerHttpInfo: '/innerhttp/info',
  saveInnerHttpInfo: '/innerhttp',
  activateInnerHttp: '/innerhttp/activate',
  removeInnerHttp: '/innerhttp/remove',

  // asset.ipv6http
  getIpv6HttpList: '/ipv6http',
  updateIpv6HttpInfo: '/ipv6http/info',
  saveIpv6HttpInfo: '/ipv6http',
  activateIpv6Http: '/ipv6http/activate',
  removeIpv6Http: '/ipv6http/remove',

  // pocvuln
  getPocVulnList: '/pocvuln',
  activatePocVuln: '/pocvuln/activate',
  removePocVuln: '/pocvuln/remove',

  // webvuln
  getWebVulnList: '/webvuln',
  activateWebVuln: '/webvuln/activate',
  removeWebVuln: '/webvuln/remove',

  // asset.cve
  getCVEList: '/cve',
  updateCVEInfo: '/cve/info',
  saveCVEInfo: '/cve',
  activateCVE: '/cve/activate',
  removeCVE: '/cve/remove',

  // asset.whitehost
  getWhiteHostList: '/whitehost',
  updateWhiteHostInfo: '/whitehost/info',
  saveWhiteHostInfo: '/whitehost',
  removeWhiteHost: '/whitehost/remove',

  // asset.cgi
  getCGIList: '/cgi',
  updateCGIInfo: '/cgi/info',
  saveCGIInfo: '/cgi',
  activateCGI: '/cgi/activate',
  removeCGI: '/cgi/remove',

  // asset.zone
  getZoneList: '/zone',
  updateZoneInfo: '/zone/info',
  saveZoneInfo: '/zone',
  removeZone: '/zone/remove'
}

export default api
