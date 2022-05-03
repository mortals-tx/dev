import api from '@/api/index'
import { axios } from '@/utils/request'

export function getInnerHostList (parameter) {
  return axios({
    url: api.getInnerHostList,
    method: 'get',
    params: parameter
  })
}

export function getInnerHostService (parameter) {
  return axios({
    url: api.getInnerHostService,
    method: 'get',
    params: parameter
  })
}

export function updateInnerHostInfo (parameter) {
  return axios({
    url: api.updateInnerHostInfo,
    method: 'post',
    data: parameter
  })
}

export function saveInnerHostInfo (parameter) {
  return axios({
    url: api.saveInnerHostInfo,
    method: 'post',
    data: parameter
  })
}

export function activateInnerHost (parameter) {
  return axios({
    url: api.activateInnerHost,
    method: 'post',
    data: parameter
  })
}

export function removeInnerHost (parameter) {
  return axios({
    url: api.removeInnerHost,
    method: 'post',
    data: parameter
  })
}
