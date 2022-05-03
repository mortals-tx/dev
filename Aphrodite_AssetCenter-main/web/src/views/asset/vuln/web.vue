<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form layout="inline" :form="filterForm">
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="Host">
              <a-input
                v-model="filterParams.host"
                placeholder="请输入Host关键字"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="plugin">
              <a-input
                v-model="filterParams.plugin"
                placeholder="请输入关键字"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="状态">
              <a-select v-model="filterParams.status" placeholder="请选择">
                <a-select-option value="0">忽略中</a-select-option>
                <a-select-option value="1">使用中</a-select-option>
                <a-select-option value="2">全部</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>

          <a-col :md="6" :sm="24">
            <span class="table-page-search-submitButtons">
              <a-button
                type="primary"
                @click="loadData"
                :loading="state.searchBtn"
                :disabled="state.searchBtn"
              >查询</a-button
              >
              <a-button
                style="margin-left: 8px"
                @click="() => (this.filterParams = {})"
              >重置</a-button
              >
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>

    <a-table
      :dataSource="webData"
      :expandRowByClick="true"
      rowKey="id"
      @expand="onExpand"
      :loading="loading"
      :pagination="false"
    >
      <div slot="expandedRowRender" slot-scope="record" style="margin: 0">
        <a-descriptions
          bordered
          class="expand-detail"
          :column="1"
          size="middle"
        >
          <a-descriptions-item
            v-for="item in record.expand"
            :key="item.key"
            :label="item.key"
            :span="1"
          >
            <template v-if="item.key.startsWith('Response')">
              <pre style="max-height: 600px; max-width: 100%">{{
                item.value
              }}</pre>
            </template>
            <template v-else-if="item.key === 'URL'">
              <a :href="item.value" target="_blank">{{ item.value }}</a>
            </template>
            <template v-else>
              <pre>{{ item.value }}</pre>
            </template>
            <a
              @click="$copy(item.value)"
              v-if="item.key.startsWith('Request')"
            >Copy</a
            >
          </a-descriptions-item>
        </a-descriptions>
      </div>
      <a-table-column
        title="ID"
        width="64px"
        :customRender="(text, record, index) => index + 1"
        key="id"
      >
      </a-table-column>
      <a-table-column
        title="Target"
        key="target"
        :sorter="(a, b) => a.target.url.localeCompare(b.target.url)"
      >
        <template slot-scope="record">
          <a
            :href="record.target.url"
            style="display: inline-block; max-width: 50vw"
            @click.prevent.stop="window.open(record.target.url)"
          >
            {{ record.target.url }}
          </a>
        </template>
      </a-table-column>
      <a-table-column
        title="PluginName / VulnType"
        key="plugin"
        :sorter="
          (a, b) =>
            (a.plugin + a.vuln_class).localeCompare(b.plugin + b.vuln_class)
        "
        :filters="vulnTypes"
        class="filter-column"
        @filter="(value, record) => record.plugin.includes(value)"
      >
        <template slot-scope="record">
          {{
            record.plugin + (record.vuln_class ? `/${record.vuln_class}` : '')
          }}
        </template>
      </a-table-column>
      <a-table-column
        title="CreateTime"
        key="create_time"
        :sorter="(a, b) => a.create_time - b.create_time"
      >
        <template slot-scope="record">
          {{ dateFormat(record.create_time) }}
        </template>
      </a-table-column>
      <a-table-column title="操作">
        <template slot-scope="record">
          <a
            v-action:remove
            v-show="record.status === 1"
            :key="record.uid"
            @click="handleRemoveWebVuln(record)"
            :loading="state.removeBtn"
            :disabled="state.removeBtn"
          >忽略</a
          >
          <a
            v-show="record.status !== 1"
            v-action:activate
            @click="handleActivateWebVuln(record)"
            :loading="state.activateBtn"
            :disabled="state.activateBtn"
          >激活</a
          >
          <a-divider type="vertical" />
          <a
            v-action:update_info
            @click="showUpdateInfoEditor(record)"
            :loading="state.updateInfoBtn"
            :disabled="state.updateInfoBtn"
          >编辑</a
          >
        </template>
      </a-table-column></a-table
    >
  </a-card>
</template>

<script>
import { STable } from '@/components'
import {
  activateWebVuln,
  getWebVulnList,
  removeWebVuln
} from '@/api/manager/asset/vuln/web'

export default {
  name: 'WebVuln',
  components: {
    STable
  },
  data () {
    return {
      webData: [],
      parameter: {},
      infoForm: null,
      infoParams: {},
      filterForm: this.$form.createForm(this),
      filterParams: {},
      state: {
        infoFormVisible: false,
        optionAlertSHow: true,
        searchBtn: false,
        activateBtn: false,
        removeBtn: false,
        updateInfoBtn: false,
        isSaveInfoEditor: false
      },
      pageSize: 10,
      paginationOption: {
        pageSizeOptions: ['10', '30', '100', '1000']
      },
      columns: [
        {
          title: 'Host',
          dataIndex: 'host'
        },
        {
          title: 'Plugin',
          dataIndex: 'plugin'
        },
        {
          title: '发现时间',
          dataIndex: 'utc_created'
        },
        {
          title: '操作',
          width: '150px',
          scopedSlots: { customRender: 'action' }
        }
      ],
      selectedRowKeys: [],
      selectedRows: [],
      options: {
        alert: {
          show: true,
          clear: () => {
            this.selectedRowKeys = []
          }
        },
        rowSelection: {
          selectedRowKeys: this.selectedRowKeys,
          onChange: this.onSelectChange
        }
      }
    }
  },
  mounted () {
    this.loadData()
  },
  computed: {
    vulnTypes () {
      const s = new Set()
      for (const vuln of this.webData) {
        s.add(vuln.plugin)
      }
      const result = []
      for (const t of s.values()) {
        result.push({ text: t, value: t })
      }
      return result
    }
  },
  filters: {
    statusFilter (status) {
      const statusMap = {
        1: '正常',
        0: '忽略'
      }
      return statusMap[status]
    }
  },
  methods: {
    loadData () {
      const params = Object.assign(this.parameter, this.filterParams)
      return getWebVulnList(params).then((response) => {
        const msg = response.msg.data
        const resData = msg.map((item) => {
          item.info.uid = item.uid
          item.info.status = item.status
          return item.info
        })
        console.log(resData)
        this.pageSize = msg.pageSize
        this.webData = resData
      })
    },
    tableOption () {
      if (!this.state.optionAlertShow) {
        this.options = {
          alert: {
            show: true,
            clear: () => {
              this.selectedRowKeys = []
            }
          },
          rowSelection: {
            selectedRowKeys: this.selectedRowKeys,
            onChange: this.onSelectChange
          }
        }
        this.state.optionAlertShow = true
      } else {
        this.options = {
          alert: false,
          rowSelection: null
        }
        this.state.optionAlertShow = false
      }
    },
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
    },
    handleActivateWebVuln (record) {
      this.state.activateBtn = true
      activateWebVuln({ uid: record.uid }).then((response) => {
        this.loadData()
      })
      this.state.activateBtn = false
    },
    handleRemoveWebVuln (record) {
      this.state.removeBtn = true
      removeWebVuln({ uid: record.uid }).then((response) => {
        this.loadData()
      })
      this.state.removeBtn = false
    },
    showSaveInfoEditor () {
      this.infoParams = {}
      this.state.isSaveInfoEditor = true
      this.state.infoFormVisible = true
    },
    showUpdateInfoEditor (record) {
      this.infoParams = Object.assign({}, record)
      this.state.isSaveInfoEditor = false
      this.state.infoFormVisible = true
    },
    handleOk () {
      this.state.infoFormVisible = false
    },
    dateFormat: function (time) {
      var date = new Date(time)
      var year = date.getFullYear()
      var month =
        date.getMonth() + 1 < 10
          ? '0' + (date.getMonth() + 1)
          : date.getMonth() + 1
      var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate()
      var hours = date.getHours() < 10 ? '0' + date.getHours() : date.getHours()
      var minutes =
        date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()
      var seconds =
        date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
      // 拼接
      return (
        year +
        '-' +
        month +
        '-' +
        day +
        ' ' +
        hours +
        ':' +
        minutes +
        ':' +
        seconds
      )
    },
    onExpand (expanded, record) {
      if (record.expand) {
        return
      }
      const detail = record.detail
      const extra = record.detail.extra
      const expand = []
      if (detail.addr) {
        expand.push({
          key: 'URL',
          value: detail.addr
        })
      }
      if (extra && extra.param && Object.keys(extra.param).length !== 0) {
        expand.push({
          key: 'ParamPosition',
          value: extra.param.position
        })
        expand.push({
          key: 'ParamKey',
          value: extra.param.key
        })
      }
      if (detail.payload) {
        expand.push({
          key: 'Payload',
          value: detail.payload
        })
      }
      if (detail.snapshot) {
        let i = 1
        for (const flow of detail.snapshot) {
          if (flow.length !== 0) {
            expand.push({
              key: 'Request' + i.toString(),
              value: flow[0]
            })
            expand.push({
              key: 'Response' + i.toString(),
              value: flow[1]
            })
            i++
          }
        }
      }
      const blankList = ['param', 'payload', 'addr']
      const shouldIgnore = function (word) {
        for (const s of blankList) {
          if (word.includes(s)) {
            return true
          }
        }
        return false
      }
      const others = {}
      for (const [k, v] of Object.entries(detail.extra)) {
        if (shouldIgnore(k)) {
          continue
        }
        others[k] = v
      }
      if (Object.keys(others).length !== 0) {
        expand.push({
          key: 'Extra',
          value: others
        })
      }
      record.expand = expand
    }
  }
}
</script>

<style scoped></style>
