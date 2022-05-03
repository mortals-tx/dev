import api from '@/api/index'
import { axios } from '@/utils/request'

export function getWebVulnList (parameter) {
  return axios({
    url: api.getWebVulnList,
    method: 'get',
    params: parameter
  })
}

export function activateWebVuln (parameter) {
  return axios({
    url: api.activateWebVuln,
    method: 'post',
    data: parameter
  })
}

export function removeWebVuln (parameter) {
  return axios({
    url: api.removeWebVuln,
    method: 'post',
    data: parameter
  })
}
