import api from '@/api/index'
import { axios } from '@/utils/request'

export function getHttpList (parameter) {
  return axios({
    url: api.getHttpList,
    method: 'get',
    params: parameter
  })
}

export function updateHttpInfo (parameter) {
  return axios({
    url: api.updateHttpInfo,
    method: 'post',
    data: parameter
  })
}

export function saveHttpInfo (parameter) {
  return axios({
    url: api.saveHttpInfo,
    method: 'post',
    data: parameter
  })
}

export function activateHttp (parameter) {
  return axios({
    url: api.activateHttp,
    method: 'post',
    data: parameter
  })
}

export function removeHttp (parameter) {
  return axios({
    url: api.removeHttp,
    method: 'post',
    data: parameter
  })
}
