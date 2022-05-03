<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="IP">
              <a-input
                v-model="filterParams.ip"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>

          <a-col :md="6" :sm="24">
            <a-form-item label="Port">
              <a-input
                v-model="filterParams.port"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="来源">
              <a-input
                v-model="filterParams.origin"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <span class="table-page-search-submitButtons">
              <a-button
                type="primary"
                @click="$refs.table.refresh(true)"
                :loading="state.searchBtn"
                :disabled="state.searchBtn"
              >查询</a-button>
              <a-button style="margin-left: 8px" @click="() => this.filterParams = {}">重置</a-button>
              <a-button v-action:save_info style="margin-left: 8px" type="primary" icon="plus" @click="showSaveInfoEditor()">新建</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>

    <div class="table-operator">
      <a-button type="dashed" @click="tableOption">{{ state.optionAlertShow && '关闭' || '开启' }} alert</a-button>
    </div>

    <s-table
      ref="table"
      :rowKey="record => record.uid"
      :pageSize.sync="pageSize"
      :columns="columns"
      :data="loadData"
      :alert="options.alert"
      :rowSelection="options.rowSelection"
      showPagination="auto"
      :pagination="paginationOption">

      <div
        slot-scope="record"
        style="margin: 0">
        <a-row
          v-if="record"
          :gutter="24"
          :style="{ marginBottom: '12px' }">
          <a-list
            bordered
            :dataSource="record"
          >
          </a-list>
        </a-row>
      </div>

      <span slot="zone" slot-scope="zone_uid">
        {{ getZoneName(zoneTree, zone_uid) }}
      </span>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-action:update_info
          @click="showUpdateInfoEditor(record)"
          :loading="state.updateInfoBtn"
          :disabled="state.updateInfoBtn"
        >编辑</a>
        <a-divider type="vertical" />
        <a
          v-action:remove
          :key="record.uid"
          @click="handleRemoveHost(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >删除</a>
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
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="唯一识别码"
        >
          <a-input placeholder="唯一识别码" v-model="infoParams.uid" id="no" disabled="disabled"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="ip"
        >
          <a-input placeholder="IP" v-model="infoParams.ip" id="ip"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="port"
        >
          <a-input placeholder="端口,若不需要针对特殊端口可不填" v-model="infoParams.port" id="port"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="origin"
        >
          <a-input placeholder="来源（蜜罐、前置、代理等）" v-model="infoParams.origin" id="host_origin"/>
        </a-form-item>

      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import {
  getWhiteHostList,
  updateWhiteHostInfo,
  saveWhiteHostInfo,
  removeWhiteHost
} from '@/api/manager/asset/whitehost/whitehost'

export default {
  name: 'WhiteHost',
  components: {
    STable
  },

  data () {
    return {
      name: 'WhiteHost',
      infoForm: null,
      infoParams: {},
      filterForm: this.$form.createForm(this),
      filterParams: {},
      pageSize: 10,
      paginationOption: {
        pageSizeOptions: ['10', '30', '100', '1000']
      },
      columns: [

        {
          title: 'ip',
          dataIndex: 'ip'
        },
        {
          title: 'port',
          dataIndex: 'port'
        },
        {
          title: '来源',
          dataIndex: 'origin'
        },
        {
          title: '添加时间',
          dataIndex: 'utc_created'
        },
        {
          title: '修改时间',
          dataIndex: 'utc_modified'
        },
        {
          title: '操作',
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: parameter => {
        const params = Object.assign(parameter, this.filterParams)
        return getWhiteHostList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.per_page
          return msg
        })
      },
      selectedRowKeys: [],
      selectedRows: [],
      options: {
        alert: { show: true, clear: () => { this.selectedRowKeys = [] } },
        rowSelection: {
          selectedRowKeys: this.selectedRowKeys,
          onChange: this.onSelectChange
        }
      },
      state: {
        infoFormVisible: false,
        searchServiceInfoBtn: false,
        serviceInfoVisible: false,
        optionAlertShow: true,
        searchBtn: false,
        activateBtn: false,
        removeBtn: false,
        updateInfoBtn: false,
        isSaveInfoEditor: false
      },
      currentHostUid: undefined,
      collapseActiveKey: ['1']

    }
  },
  methods: {
    recursionZones (zones, key) {
      const data = []
      for (const zone of zones) {
        const item = {}
        item.key = key + zone.parent.name
        item.value = zone.parent.uid
        item.title = zone.parent.name
        if (zone.children) {
          item['children'] = this.recursionZones(zone.children, item.key + '-')
        }
        data.push(item)
      }
      return data
    },
    getZoneName (zones, uid) {
      if (uid === null) {
        return ''
      }
      for (const zone of zones) {
        if (zone.value === uid) {
          return zone.key
        } else {
          if (zone.children) {
            const value = this.getZoneName(zone.children, uid)
            if (value !== undefined) {
              return value
            }
          }
        }
      }
    },
    tableOption () {
      if (!this.state.optionAlertShow) {
        this.options = {
          alert: { show: true, clear: () => { this.selectedRowKeys = [] } },
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
    handleRemoveHost (record) {
      this.state.removeBtn = true
      this.$confirm('确定要删除该记录吗 ?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          removeWhiteHost({ 'uid': record.uid }).then(response => {
            this.$refs['table'].refresh(true)
          })
        })
      this.state.removeBtn = false
    },
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
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
        saveWhiteHostInfo(this.infoParams).then(response => {
          this.$message({
            message: 'success',
            type: 'success'
          })
          this.$refs.table.refresh()
        })
      } else {
        updateWhiteHostInfo(this.infoParams).then(response => {
          this.$message({
            message: 'success',
            type: 'success'
          })
          this.$refs.table.refresh()
        })
      }
      this.state.infoFormVisible = false
    },
    changeActiveKey (key) {
      if (key.length !== 0) {
        this.currentHostUid = key[0]
        for (const refs in this.$refs) {
          if (refs === key[0]) {
            this.$refs[refs].refresh(true)
          }
        }
      }
    }
  }
}
</script>

<style scoped>

</style>
