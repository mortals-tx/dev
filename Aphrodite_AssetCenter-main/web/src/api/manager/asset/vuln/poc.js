import api from '@/api/index'
import { axios } from '@/utils/request'

export function getPocVulnList (parameter) {
  return axios({
    url: api.getPocVulnList,
    method: 'get',
    params: parameter
  })
}

export function activatePocVuln (parameter) {
  return axios({
    url: api.activatePocVuln,
    method: 'post',
    data: parameter
  })
}

export function removePocVuln (parameter) {
  return axios({
    url: api.removePocVuln,
    method: 'post',
    data: parameter
  })
}
