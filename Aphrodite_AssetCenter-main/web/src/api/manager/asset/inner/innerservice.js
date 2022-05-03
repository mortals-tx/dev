import api from '@/api/index'
import { axios } from '@/utils/request'

export function getInnerServiceList (parameter) {
  return axios({
    url: api.getInnerServiceList,
    method: 'get',
    params: parameter
  })
}
