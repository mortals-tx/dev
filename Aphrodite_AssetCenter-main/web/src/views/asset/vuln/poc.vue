<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form layout="inline" :form="filterForm">
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="Host">
              <a-input v-model="filterParams.host" placeholder="请输入Host关键字" />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="Poc">
              <a-input v-model="filterParams.template_id" placeholder="请输入关键字" />
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
                @click="$refs.table.refresh(true)"
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

    <s-table
      :columns="columns"
      :data="loadData"
      :alert="options.alert"
      :rowSelection="options.rowSelection"
      :pageSize.sync="pageSize"
      ref="table"
      :rowKey="record => record.uid"
      showPagination="auto"
      :pagination="paginationOption"
    >
      <pre slot="expandedRowRender" slot-scope="record" style="margin: 0; white-space: pre-wrap; word-wrap: break-word;">{{
        record.info
      }}</pre>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemovePocVuln(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >忽略</a>
        <a
          v-action:activate
          v-show="record.status !== 1"
          @click="handleActivatePocVuln(record)"
          :loading="state.activateBtn"
          :disabled="state.activateBtn"
        >恢复</a
        >
      </span>
    </s-table>

  </a-card>
</template>

<script>
import { STable } from '@/components'
import {
  activatePocVuln,
  getPocVulnList,
  removePocVuln
} from '@/api/manager/asset/vuln/poc'

export default {
  name: 'PocVuln',
  components: {
    STable
  },
  data () {
    return {
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
          title: 'Poc',
          dataIndex: 'template_id'
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
      loadData: parameter => {
        const params = Object.assign(parameter, this.filterParams)
        return getPocVulnList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          return msg
        })
      },
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
    handleActivatePocVuln (record) {
      this.state.activateBtn = true
      activatePocVuln({ uid: record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemovePocVuln (record) {
      this.state.removeBtn = true
      removePocVuln({ uid: record.uid }).then(response => {
        this.$refs.table.refresh(true)
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
    }
  }
}
</script>

<style scoped></style>
