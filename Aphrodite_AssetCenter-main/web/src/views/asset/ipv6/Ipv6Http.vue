<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="website">
              <a-input
                v-model="filterParams.website"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="Ipv6Http状态">
              <a-input
                v-model="filterParams.http_status"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="title">
              <a-input
                v-model="filterParams.title"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="CMS">
              <a-input
                v-model="filterParams.cms"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="状态">
              <a-select
                v-model="filterParams.status"
                placeholder="请选择"
              >
                <a-select-option value="0">禁用中</a-select-option>
                <a-select-option value="1">使用中</a-select-option>
                <a-select-option value="2">全部</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="product">
              <a-input
                v-model="filterParams.product"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          </a-col>
          <a-col :md="7" :sm="24">
            <a-form-item label="发现时间">
              <el-date-picker
                size="mini"
                v-model="filterParams.utc_created"
                type="datetime"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                placeholder="选择日期时间">
              </el-date-picker>
            </a-form-item>
          </a-col>
          <a-col :md="5" :sm="24">
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
      :columns="columns"
      :data="loadData"
      :alert="options.alert"
      :rowSelection="options.rowSelection"
      :pageSize.sync="pageSize"
      ref="table"
      :rowKey="record => record.uid"
      showPagination="auto"
      :pagination="paginationOption">

      <pre slot="expandedRowRender" slot-scope="record" style="margin: 0">{{ record.info }}</pre>

      <span slot="zone" slot-scope="zone_uid">
        {{ getZoneName(zoneTree, zone_uid) }}
      </span>

      <span slot="utc_created" slot-scope="text">
        {{ text }}
      </span>

      <a target="_blank" :href="text" slot="website" slot-scope="text">{{ text }}</a>

      <span slot="action" slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemoveIpv6Http(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-show="record.status !== 1"
          v-action:activate
          @click="handleActivateIpv6Http(record)"
          :loading="state.activateBtn"
          :disabled="state.activateBtn"
        >激活</a>
        <a-divider type="vertical" />
        <a
          v-action:update_info
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
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="唯一识别码"
        >
          <a-input placeholder="唯一识别码" v-model="infoParams.uid" id="no" disabled="disabled"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          v-show="state.isSaveInfoEditor"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="website"
        >
          <a-input placeholder="website" v-model="infoParams.website" id="http_website"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="http_status"
        >
          <a-input placeholder="http_status" v-model="infoParams.http_status" id="http_status"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="title"
        >
          <a-input placeholder="title" v-model="infoParams.title" id="http_title"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="cms"
        >
          <a-input placeholder="cms" v-model="infoParams.cms" id="http_cms"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="product"
        >
          <a-input placeholder="业务产品" v-model="infoParams.product" id="http_product"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="info"
          hasFeedback
        >
          <a-input placeholder="Json格式" type="textarea" v-if="state.isSaveInfoEditor" v-model="infoParams.info" />
          <pre v-else>{{ infoParams.info }}</pre>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import { activateIpv6Http, getIpv6HttpList, removeIpv6Http, saveIpv6HttpInfo, updateIpv6HttpInfo } from '@/api/manager/asset/ipv6/ipv6http'

export default {
  name: 'Ipv6Http',
  components: {
    STable
  },
  data () {
    return {
      infoForm: null,
      infoParams: {},
      filterForm: this.$form.createForm(this),
      filterParams: {},
      zoneTree: [],
      state: {
        infoFormVisible: false,
        optionAlertShow: true,
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
          title: 'website',
          dataIndex: 'website',
          scopedSlots: { customRender: 'website' }
        },
        {
          title: 'Http状态',
          dataIndex: 'http_status'
        },
        {
          title: '标题',
          dataIndex: 'title'
        },
        {
          title: 'CMS',
          dataIndex: 'cms'
        },
        {
          title: '产品',
          dataIndex: 'product'
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
        return getIpv6HttpList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          this.zoneTree = this.recursionZones(msg.zones, '')
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
      }
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
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
    },
    handleActivateIpv6Http (record) {
      this.state.activateBtn = true
      activateIpv6Http({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemoveIpv6Http (record) {
      this.state.removeBtn = true
      removeIpv6Http({ 'uid': record.uid }).then(response => {
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
        saveIpv6HttpInfo(this.infoParams).then(response => {
          this.$message({
            message: 'success',
            type: 'success'
          })
          this.$refs.table.refresh()
        }).catch(response => {
          this.$message({
            message: response,
            type: 'error'
          })
        })
      } else {
        updateIpv6HttpInfo(this.infoParams).then(response => {
          this.$message({
            message: 'success',
            type: 'success'
          })
          this.$refs.table.refresh()
        }).catch(response => {
          this.$message({
            message: response,
            type: 'error'
          })
        })
      }
      this.state.infoFormVisible = false
    }
  }
}
</script>

<style scoped>

</style>
