import api from '@/api/index'
import { axios } from '@/utils/request'

export function getIpv6HostList (parameter) {
  return axios({
    url: api.getIpv6HostList,
    method: 'get',
    params: parameter
  })
}

export function getIpv6HostService (parameter) {
  return axios({
    url: api.getIpv6HostService,
    method: 'get',
    params: parameter
  })
}

export function updateIpv6HostInfo (parameter) {
  return axios({
    url: api.updateIpv6HostInfo,
    method: 'post',
    data: parameter
  })
}

export function saveIpv6HostInfo (parameter) {
  return axios({
    url: api.saveIpv6HostInfo,
    method: 'post',
    data: parameter
  })
}

export function activateIpv6Host (parameter) {
  return axios({
    url: api.activateIpv6Host,
    method: 'post',
    data: parameter
  })
}

export function removeIpv6Host (parameter) {
  return axios({
    url: api.removeIpv6Host,
    method: 'post',
    data: parameter
  })
}
