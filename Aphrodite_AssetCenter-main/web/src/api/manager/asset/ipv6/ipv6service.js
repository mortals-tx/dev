import api from '@/api/index'
import { axios } from '@/utils/request'

export function getIpv6ServiceList (parameter) {
  return axios({
    url: api.getIpv6ServiceList,
    method: 'get',
    params: parameter
  })
}
