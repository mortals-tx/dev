import api from '@/api/index'
import { axios } from '@/utils/request'

export function getIpv6HttpList (parameter) {
  return axios({
    url: api.getIpv6HttpList,
    method: 'get',
    params: parameter
  })
}

export function updateIpv6HttpInfo (parameter) {
  return axios({
    url: api.updateIpv6HttpInfo,
    method: 'post',
    data: parameter
  })
}

export function saveIpv6HttpInfo (parameter) {
  return axios({
    url: api.saveIpv6HttpInfo,
    method: 'post',
    data: parameter
  })
}

export function activateIpv6Http (parameter) {
  return axios({
    url: api.activateIpv6Http,
    method: 'post',
    data: parameter
  })
}

export function removeIpv6Http (parameter) {
  return axios({
    url: api.removeIpv6Http,
    method: 'post',
    data: parameter
  })
}
