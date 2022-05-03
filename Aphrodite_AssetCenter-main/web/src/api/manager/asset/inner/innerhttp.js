import api from '@/api/index'
import { axios } from '@/utils/request'

export function getInnerHttpList (parameter) {
  return axios({
    url: api.getInnerHttpList,
    method: 'get',
    params: parameter
  })
}

export function updateInnerHttpInfo (parameter) {
  return axios({
    url: api.updateInnerHttpInfo,
    method: 'post',
    data: parameter
  })
}

export function saveInnerHttpInfo (parameter) {
  return axios({
    url: api.saveInnerHttpInfo,
    method: 'post',
    data: parameter
  })
}

export function activateInnerHttp (parameter) {
  return axios({
    url: api.activateInnerHttp,
    method: 'post',
    data: parameter
  })
}

export function removeInnerHttp (parameter) {
  return axios({
    url: api.removeInnerHttp,
    method: 'post',
    data: parameter
  })
}
