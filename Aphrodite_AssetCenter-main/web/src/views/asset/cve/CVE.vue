<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form layout="inline" :form="filterForm">
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="编号">
              <a-input
                v-model="filterParams.cve_id"
                placeholder="请输入编号关键字"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="漏洞名称">
              <a-input
                v-model="filterParams.cve_name"
                placeholder="请输入关键字"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="漏洞类型">
              <a-input
                v-model="filterParams.cve_type"
                placeholder="请输入关键字"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="漏洞状态">
              <a-input
                v-model="filterParams.cve_status"
                placeholder="请输入关键字"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="来源">
              <a-input
                v-model="filterParams.cve_from"
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
          <a-col :md="7" :sm="24">
            <a-form-item label="披露时间">
              <el-date-picker
                size="mini"
                v-model="filterParams.cve_time"
                type="datetime"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                placeholder="选择日期时间"
              >
              </el-date-picker>
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
              <a-button
                v-action:save_info
                style="margin-left: 8px"
                type="primary"
                @click="showSaveInfoEditor()"
              >新建</a-button
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
      :rowKey="(record) => record.uid"
      showPagination="auto"
      :pagination="paginationOption"
    >

      <span slot="cve_id" slot-scope="record">
        <a :href="record.cve_url" target="_blank">{{ record.cve_id }}</a>
      </span>

      <span slot="cve_name" slot-scope="record">
        <a :href="record.cve_url" target="_blank">{{ record.cve_name }}</a>
      </span>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemoveCVE(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >忽略</a
        >
        <a
          v-action:activate
          v-show="record.status !== 1"
          @click="handleActivateCVE(record)"
          :loading="state.activateBtn"
          :disabled="state.activateBtn"
        >恢复</a
        >
        <a-divider v-show="record.status === 1" type="vertical" />
        <a
          v-action:update_info
          v-show="record.status === 1"
          @click="showUpdateInfoEditor(record)"
          :loading="state.updateInfoBtn"
          :disabled="state.updateInfoBtn"
        >编辑</a>
      </span>
    </s-table>
    <a-modal
      title="编辑"
      :width="1000"
      v-model="state.infoFormVisible"
      @ok="handleOk"
    >
      <a-form :form="infoForm">
        <a-form-item
          v-show="!state.isSaveInfoEditor"
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="唯一识别码"
        >
          <a-input
            placeholder="唯一识别码"
            v-model="infoParams.uid"
            id="no"
            disabled="disabled"
          />
        </a-form-item>

        <a-form-item
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="漏洞编号"
        >
          <a-input
            placeholder="漏洞编号"
            v-model="infoParams.cve_id"
            id="cve_id"
          />
        </a-form-item>

        <a-form-item
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="漏洞链接"
        >
          <a-input
            placeholder="漏洞链接"
            v-model="infoParams.cve_url"
            id="cve_url"
          />
        </a-form-item>

        <a-form-item
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="漏洞名称"
        >
          <a-input
            placeholder="漏洞名称"
            v-model="infoParams.cve_name"
            id="cve_name"
          />
        </a-form-item>

        <a-form-item
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="漏洞类型"
        >
          <a-input
            placeholder="漏洞类型"
            v-model="infoParams.cve_type"
            id="cve_type"
          />
        </a-form-item>
        <a-form-item
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="漏洞状态"
        >
          <a-input
            placeholder="漏洞状态"
            v-model="infoParams.cve_status"
            id="cve_status"
          />
        </a-form-item>
        <a-form-item
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="来源"
        >
          <a-input
            placeholder="来源"
            v-model="infoParams.cve_from"
            id="cve_from"
          />
        </a-form-item>
        <a-form-item
          :labelCol="{ xs: { span: 24 }, sm: { span: 5 } }"
          :wrapperCol="{ xs: { span: 24 }, sm: { span: 16 } }"
          label="披露时间"
        >
          <el-date-picker
            size="mini"
            v-model="infoParams.cve_time"
            type="datetime"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            placeholder="选择日期时间"
          >
          </el-date-picker>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import { activateCVE, updateCVEInfo, saveCVEInfo, getCVEList, removeCVE } from '@/api/manager/asset/cve/cve'

export default {
  name: 'CVE',
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
          title: '漏洞编号',
          key: 'cve_id',
          scopedSlots: { customRender: 'cve_id' }
        },
        {
          title: '漏洞名称',
          // dataIndex: 'cve_name'
          scopedSlots: { customRender: 'cve_name' }
        },
        {
          title: '漏洞类型',
          dataIndex: 'cve_type'
        },
        {
          title: '漏洞状态',
          dataIndex: 'cve_status'
        },
        {
          title: '披露时间',
          dataIndex: 'cve_time'
        },
        {
          title: '来源',
          dataIndex: 'cve_from'
        },
        {
          title: '修改时间',
          dataIndex: 'utc_modified'
        },
        {
          title: '操作',
          width: '150px',
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: (parameter) => {
        const params = Object.assign(parameter, this.filterParams)
        return getCVEList(params).then((response) => {
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
    handleActivateCVE (record) {
      this.state.activateBtn = true
      activateCVE({ uid: record.uid }).then((response) => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemoveCVE (record) {
      this.state.removeBtn = true
      removeCVE({ uid: record.uid }).then((response) => {
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
      if (this.state.isSaveInfoEditor) {
        saveCVEInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      } else {
        updateCVEInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      }
      this.state.infoFormVisible = false
    }
  }
}
</script>

<style scoped></style>
