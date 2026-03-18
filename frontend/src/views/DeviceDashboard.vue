<template>
  <a-layout class="device-dashboard">
    <!-- 侧边栏 -->
    <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible>
      <div class="logo">
        <icon-robot class="logo-icon" />
        <span v-if="!collapsed">MDM 控制台</span>
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item key="dashboard">
          <icon-dashboard />
          <span>设备大盘</span>
        </a-menu-item>
        <a-menu-item key="ota">
          <icon-upload />
          <span>OTA 固件</span>
        </a-menu-item>
        <a-menu-item key="settings">
          <icon-settings />
          <span>系统设置</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <!-- 主内容区 -->
    <a-layout>
      <a-layout-header class="header">
        <div class="header-left">
          <menu-unfold-outlined
            v-if="collapsed"
            class="trigger"
            @click="collapsed = !collapsed"
          />
          <menu-fold-outlined v-else class="trigger" @click="collapsed = !collapsed" />
        </div>
        <div class="header-right">
          <a-badge :count="warningCount" :offset="[-5, 5]">
            <icon-bell style="font-size: 20px; cursor: pointer;" />
          </a-badge>
        </div>
      </a-layout-header>

      <a-layout-content class="content">
        <!-- 统计看板 -->
        <a-row :gutter="16" class="stats-row">
          <a-col :span="8">
            <a-card>
              <a-statistic
                title="总设备数"
                :value="stats.total"
                :prefix="h(createFromIconfontCN('icon-robot'))"
              />
            </a-card>
          </a-col>
          <a-col :span="8">
            <a-card>
              <a-statistic
                title="当前在线"
                :value="stats.online"
                :value-style="{ color: '#52c41a' }"
                :prefix="h(createFromIconfontCN('icon-check-circle'))"
              />
            </a-card>
          </a-col>
          <a-col :span="8">
            <a-card>
              <a-statistic
                title="离线告警"
                :value="stats.offline"
                :value-style="{ color: '#ff4d4f' }"
                :prefix="h(createFromIconfontCN('icon-warning'))"
              />
            </a-card>
          </a-col>
        </a-row>

        <!-- 设备列表 -->
        <a-card class="device-table-card">
          <template #title>
            <div class="table-title">
              <span>设备列表</span>
              <a-button type="primary" @click="loadDevices">
                <template #icon><icon-refresh /></template>
                刷新
              </a-button>
            </div>
          </template>

          <a-table
            :columns="columns"
            :data="devices"
            :loading="loading"
            :pagination="pagination"
            :filter-configs="filterConfigs"
            @change="handleTableChange"
            row-key="device_id"
          >
            <!-- 在线状态列 -->
            <template #isOnline="{ record }">
              <a-badge
                :status="record.is_online ? 'processing' : 'danger'"
                :text="record.is_online ? '在线' : '离线'"
              />
            </template>

            <!-- 电量列 -->
            <template #batteryLevel="{ record }">
              <a-progress
                :percent="record.battery_level || 0"
                :stroke-width="6"
                :color="getBatteryColor(record.battery_level)"
                style="width: 100px;"
              />
            </template>

            <!-- 操作列 -->
            <template #operations="{ record }">
              <a-button type="primary" size="small" @click="openCommandDrawer(record)">
                指令控制
              </a-button>
            </template>
          </a-table>
        </a-card>

        <!-- 指令控制抽屉 -->
        <a-drawer
          v-model:visible="drawerVisible"
          title="指令控制"
          width="400"
          placement="right"
        >
          <a-form v-if="currentDevice" :model="commandForm" layout="vertical">
            <a-form-item label="设备ID">
              <a-input :value="currentDevice.device_id" disabled />
            </a-form-item>
            <a-form-item label="SN码">
              <a-input :value="currentDevice.sn_code" disabled />
            </a-form-item>
            <a-form-item label="指令类型">
              <a-select v-model="commandForm.cmd_type" placeholder="选择指令类型">
                <a-option value="action">动作指令</a-option>
                <a-option value="display">显示指令</a-option>
                <a-option value="config">配置更新</a-option>
                <a-option value="ota">OTA升级</a-option>
              </a-select>
            </a-form-item>
            <a-form-item label="指令内容">
              <a-textarea
                v-model="commandForm.action"
                placeholder="输入指令内容"
                :rows="4"
              />
            </a-form-item>
            <a-form-item>
              <a-space>
                <a-button type="primary" @click="sendCommand" :loading="sending">
                  发送指令
                </a-button>
                <a-button @click="drawerVisible = false">取消</a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </a-drawer>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, h, createVNode } from 'vue';
import { Message } from '@arco-design/web-vue';
import axios from 'axios';
import { IconRobot, IconDashboard, IconUpload, IconSettings, IconRefresh, IconBell, IconCheckCircle, IconWarning } from '@arco-design/web-vue/es/icon';

// 扩展 Icon 类型
const IconDashboard1 = IconDashboard;
const IconUpload1 = IconUpload;
const IconSettings1 = IconSettings;
const IconRefresh1 = IconRefresh;
const IconBell1 = IconBell;
const IconCheckCircle1 = IconCheckCircle;
const IconWarning1 = IconWarning;

// 类型定义
interface Device {
  device_id: string;
  mac_address: string;
  sn_code: string;
  hardware_model: string;
  firmware_version: string;
  bind_user_id?: string;
  lifecycle_status: number;
  is_online: boolean;
  battery_level: number;
  current_mode: string;
  created_at: string;
  updated_at: string;
}

interface Pagination {
  current: number;
  pageSize: number;
  total: number;
}

// 响应式状态
const collapsed = ref(false);
const selectedKeys = ref(['dashboard']);
const loading = ref(false);
const devices = ref<Device[]>([]);
const drawerVisible = ref(false);
const currentDevice = ref<Device | null>(null);
const sending = ref(false);

const commandForm = reactive({
  cmd_type: 'action',
  action: ''
});

// 统计
const stats = reactive({
  total: 0,
  online: 0,
  offline: 0
});
const warningCount = ref(0);

// 分页
const pagination = reactive<Pagination>({
  current: 1,
  pageSize: 20,
  total: 0
});

// 表格列定义
const columns = [
  {
    title: '设备ID',
    dataIndex: 'device_id',
    width: 180,
    ellipsis: true
  },
  {
    title: 'SN码',
    dataIndex: 'sn_code',
    width: 120
  },
  {
    title: '硬件型号',
    dataIndex: 'hardware_model',
    width: 120
  },
  {
    title: '电量',
    dataIndex: 'battery_level',
    width: 120,
    slotName: 'batteryLevel'
  },
  {
    title: '固件版本',
    dataIndex: 'firmware_version',
    width: 100
  },
  {
    title: '在线状态',
    dataIndex: 'is_online',
    width: 100,
    slotName: 'isOnline',
    filters: [
      { text: '在线', value: 'online' },
      { text: '离线', value: 'offline' }
    ]
  },
  {
    title: '操作',
    slotName: 'operations',
    width: 120,
    fixed: 'right'
  }
];

// 筛选配置
const filterConfigs = [
  {
    dataIndex: 'is_online',
    filters: [
      { label: '在线', value: 'online' },
      { label: '离线', value: 'offline' }
    ]
  }
];

// 加载设备列表
const loadDevices = async () => {
  loading.value = true;
  try {
    const params = {
      page: pagination.current,
      page_size: pagination.pageSize
    };
    
    const response = await axios.get('/api/v1/devices/list', { params });
    const { data } = response.data;
    
    devices.value = data.list;
    pagination.total = data.pagination.total;
    
    // 更新统计
    stats.total = data.pagination.total;
    stats.online = data.list.filter((d: Device) => d.is_online).length;
    stats.offline = stats.total - stats.online;
    warningCount.value = stats.offline;
    
  } catch (error) {
    Message.error('加载设备列表失败');
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 表格变化处理
const handleTableChange = (pag: Pagination) => {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  loadDevices();
};

// 打开指令抽屉
const openCommandDrawer = (device: Device) => {
  currentDevice.value = device;
  commandForm.cmd_type = 'action';
  commandForm.action = '';
  drawerVisible.value = true;
};

// 发送指令
const sendCommand = async () => {
  if (!currentDevice.value || !commandForm.action) {
    Message.warning('请输入指令内容');
    return;
  }

  sending.value = true;
  try {
    await axios.post(`/api/v1/devices/${currentDevice.value.device_id}/command`, {
      cmd_type: commandForm.cmd_type,
      action: commandForm.action
    });
    
    Message.success('指令发送成功');
    drawerVisible.value = false;
  } catch (error) {
    Message.error('指令发送失败');
  } finally {
    sending.value = false;
  }
};

// 获取电量颜色
const getBatteryColor = (level: number | undefined): string => {
  if (!level || level <= 0) return '#ff4d4f';
  if (level < 20) return '#ff4d4f';
  if (level < 50) return '#faad14';
  return '#52c41a';
};

// 使用 IconFont
const createFromIconfontCN = (type: string) => {
  return () => createVNode('svg', {
    class: 'icon',
    'icon-font': type
  });
};

// 自动刷新定时器
let refreshTimer: number | null = null;

onMounted(() => {
  loadDevices();
  
  // 每10秒刷新一次
  refreshTimer = window.setInterval(() => {
    loadDevices();
  }, 10000);
});

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }
});
</script>

<style scoped>
.device-dashboard {
  min-height: 100vh;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  gap: 8px;
}

.logo-icon {
  font-size: 28px;
}

.header {
  background: #fff;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.trigger {
  font-size: 18px;
  cursor: pointer;
  transition: color 0.3s;
}

.trigger:hover {
  color: #165dff;
}

.content {
  margin: 16px;
}

.stats-row {
  margin-bottom: 16px;
}

.device-table-card {
  margin-top: 16px;
}

.table-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.arco-statistic-title) {
  font-size: 14px;
  color: #86909c;
}

:deep(.arco-statistic-content) {
  font-size: 28px;
}
</style>
