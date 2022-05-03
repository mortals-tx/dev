import api from '@/api/index'
import { axios } from '@/utils/request'

export function getWhiteHostList (parameter) {
  return axios({
    url: api.getWhiteHostList,
    method: 'get',
    params: parameter
  })
}

export function updateWhiteHostInfo (parameter) {
  return axios({
    url: api.updateWhiteHostInfo,
    method: 'post',
    data: parameter
  })
}

export function saveWhiteHostInfo (parameter) {
  return axios({
    url: api.saveWhiteHostInfo,
    method: 'post',
    data: parameter
  })
}

export function removeWhiteHost (parameter) {
  return axios({
    url: api.removeWhiteHost,
    method: 'post',
    data: parameter
  })
}
