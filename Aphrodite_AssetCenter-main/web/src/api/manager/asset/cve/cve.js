import api from '@/api/index'
import { axios } from '@/utils/request'

export function getCVEList (parameter) {
  return axios({
    url: api.getCVEList,
    method: 'get',
    params: parameter
  })
}

export function getCVEService (parameter) {
  return axios({
    url: api.getCVEService,
    method: 'get',
    params: parameter
  })
}

export function updateCVEInfo (parameter) {
  return axios({
    url: api.updateCVEInfo,
    method: 'post',
    data: parameter
  })
}

export function saveCVEInfo (parameter) {
  return axios({
    url: api.saveCVEInfo,
    method: 'post',
    data: parameter
  })
}

export function activateCVE (parameter) {
  return axios({
    url: api.activateCVE,
    method: 'post',
    data: parameter
  })
}

export function removeCVE (parameter) {
  return axios({
    url: api.removeCVE,
    method: 'post',
    data: parameter
  })
}
