// eslint-disable-next-line
import { UserLayout, BasicLayout, RouteView } from '@/layouts'

export const asyncRouterMap = [
  {
    path: '/',
    name: 'index',
    component: BasicLayout,
    meta: { title: '首页' },
    redirect: '/auth/user',
    children: [
      // auth
      {
        path: '/auth',
        name: 'auth',
        redirect: '/auth/permission',
        component: RouteView,
        meta: {
          title: '访问控制',
          keepAlive: true,
          icon: 'user',
          permission: [
            'manager_auth.permission',
            'manager_auth.role',
            'manager_auth.user'
          ]
        },
        children: [
          {
            path: '/auth/permission',
            name: 'Permission',
            component: () => import('@/views/auth/Permission'),
            meta: {
              title: '权限列表',
              keepAlive: true,
              permission: ['manager_auth.permission']
            }
          },
          {
            path: '/auth/role',
            name: 'Role',
            component: () => import('@/views/auth/Role'),
            meta: {
              title: '角色列表',
              keepAlive: true,
              permission: ['manager_auth.role']
            }
          },
          {
            path: '/auth/user',
            name: 'User',
            component: () => import('@/views/auth/User'),
            meta: {
              title: '用户列表',
              keepAlive: true,
              permission: ['manager_auth.user']
            }
          }
        ]
      },

      // outside 外网资产
      {
        path: '/outside',
        name: 'Outside',
        redirect: '/outside/host',
        component: RouteView,
        meta: {
          title: '外网资产',
          keepAlive: true,
          icon: 'appstore',
          permission: [
            'manager_asset.host',
            'manager_asset.domain',
            'manager_asset.service'
          ]
        },
        children: [
          {
            path: '/outside/host',
            name: 'Host',
            component: () => import('@/views/asset/outside/Host.vue'),
            meta: {
              title: 'IP列表',
              keepAlive: true,
              permission: ['manager_asset.host']
            }
          },
          {
            path: '/outside/service',
            name: 'Service',
            component: () => import('@/views/asset/outside/Service'),
            meta: {
              title: '服务列表',
              keepAlive: true,
              permission: ['manager_asset.service']
            }
          },
          {
            path: '/outside/domain',
            name: 'Domain',
            component: () => import('@/views/asset/outside/Domain'),
            meta: {
              title: '域名列表',
              keepAlive: true,
              permission: ['manager_asset.domain']
            }
          },
          {
            path: '/outside/http',
            name: 'Http',
            component: () => import('@/views/asset/outside/Http'),
            meta: {
              title: 'Http应用列表',
              keepAlive: true,
              permission: ['manager_asset.http']
            }
          }
        ]
      },

      // inner 内网资产
      {
        path: '/inner',
        name: 'Inner',
        component: RouteView,
        meta: {
          title: '内网资产',
          keepAlive: true,
          icon: 'appstore',
          permission: ['manager_asset.innerhost']
        },
        children: [
          {
            path: '/inner/innerhost',
            name: 'InnerHost',
            component: () => import('@/views/asset/inner/InnerHost'),
            meta: {
              title: 'IP列表',
              keepAlive: true,
              permission: ['manager_asset.innerhost']
            }
          },
          {
            path: '/inner/innerservice',
            name: 'InnerService',
            component: () => import('@/views/asset/inner/InnerService'),
            meta: {
              title: '服务列表',
              keepAlive: true,
              permission: ['manager_asset.innerservice']
            }
          },
          {
            path: '/inner/innerhttp',
            name: 'InnerHttp',
            component: () => import('@/views/asset/inner/InnerHttp'),
            meta: {
              title: 'Http列表',
              keepAlive: true,
              permission: ['manager_asset.innerhttp']
            }
          }
        ]
      },

      // ipv6 ipv6
      {
        path: '/ipv6',
        name: 'Ipv6',
        component: RouteView,
        meta: {
          title: 'IPV6资产',
          keepAlive: true,
          icon: 'appstore',
          permission: ['manager_asset.ipv6host']
        },
        children: [
          {
            path: '/ipv6/ipv6host',
            name: 'Ipv6Host',
            component: () => import('@/views/asset/ipv6/Ipv6Host'),
            meta: {
              title: 'IPV6列表',
              keepAlive: true,
              permission: ['manager_asset.ipv6host']
            }
          },
          {
            path: '/ipv6/ipv6service',
            name: 'Ipv6Service',
            component: () => import('@/views/asset/ipv6/Ipv6Service'),
            meta: {
              title: '服务列表',
              keepAlive: true,
              permission: ['manager_asset.ipv6service']
            }
          },
          {
            path: '/ipv6/ipv6http',
            name: 'Ipv6Http',
            component: () => import('@/views/asset/ipv6/Ipv6Http'),
            meta: {
              title: 'Http列表',
              keepAlive: true,
              permission: ['manager_asset.ipv6http']
            }
          }
        ]
      },

      // vuln
      {
        path: '/vuln',
        name: 'Vuln',
        component: RouteView,
        meta: {
          title: '漏洞信息',
          keepAlive: true,
          icon: 'appstore',
          permission: ['manager_asset.webvuln']
        },
        children: [
          {
            path: '/vuln/webvuln',
            name: 'WebVuln',
            component: () => import('@/views/asset/vuln/web'),
            meta: {
              title: 'web_xray漏洞',
              keepAlive: true,
              permission: ['manager_asset.webvuln']
            }
          },
          {
            path: '/vuln/pocvuln',
            name: 'PocVuln',
            component: () => import('@/views/asset/vuln/poc'),
            meta: {
              title: 'poc_nuclei漏洞',
              keepAlive: true,
              permission: ['manager_asset.pocvuln']
            }
          }
        ]
      },

      // CVE
      {
        path: '/asset/cve',
        name: 'CVE',
        component: () => import('@/views/asset/cve/CVE'),
        meta: {
          title: 'CVE漏洞监控',
          keepAlive: true,
          icon: 'appstore',
          permission: ['manager_asset.cve']
        }
      },

      // whitehost 白名单IP
      {
        path: '/asset/whitehost',
        name: 'WhiteHost',
        component: () => import('@/views/asset/whitehost/WhiteHost'),
        meta: {
          title: 'IP白名单列表',
          keepAlive: true,
          icon: 'appstore',
          permission: ['manager_asset.whitehost']
        }
      },

      // cgi
      {
        path: '/asset/cgi',
        name: 'CGI',
        component: () => import('@/views/asset/CGI'),
        meta: {
          title: 'CGI列表',
          keepAlive: true,
          icon: 'appstore',
          permission: ['manager_asset.cgi']
        }
      },

      // zone
      {
        path: '/asset/zone',
        name: 'Zone',
        component: () => import('@/views/asset/Zone'),
        meta: {
          title: '区域列表',
          keepAlive: true,
          icon: 'appstore',
          permission: ['manager_asset.zone']
        }
      },

      // Exception
      {
        path: '/exception',
        name: 'exception',
        component: RouteView,
        redirect: '/exception/403',
        meta: { title: '异常页', icon: 'warning', permission: ['exception'] },
        children: [
          {
            path: '/exception/403',
            name: 'Exception403',
            component: () =>
              import(/* webpackChunkName: "fail" */ '@/views/exception/403'),
            meta: { title: '403', permission: ['exception'] }
          },
          {
            path: '/exception/404',
            name: 'Exception404',
            component: () =>
              import(/* webpackChunkName: "fail" */ '@/views/exception/404'),
            meta: { title: '404', permission: ['exception'] }
          },
          {
            path: '/exception/500',
            name: 'Exception500',
            component: () =>
              import(/* webpackChunkName: "fail" */ '@/views/exception/500'),
            meta: { title: '500', permission: ['exception'] }
          }
        ]
      }
    ]
  },
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
]

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        component: () =>
          import(/* webpackChunkName: "user" */ '@/views/user/Login')
      }
    ]
  },

  {
    path: '/404',
    component: () =>
      import(/* webpackChunkName: "fail" */ '@/views/exception/404')
  }
]
