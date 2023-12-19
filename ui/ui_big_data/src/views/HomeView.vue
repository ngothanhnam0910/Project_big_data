<script setup>
import { Layout, LayoutSider, Menu, MenuItem, LayoutHeader, LayoutContent} from 'ant-design-vue';
import {
    UserOutlined, MenuFoldOutlined, MenuUnfoldOutlined
    
} from '@ant-design/icons-vue';

import Charts from '../components/Charts.vue'
import Correlations from '../components/Correlations.vue'
import Trending from '../components/Trending.vue'
import TopTrending from '../components/TopTrending.vue'
</script>

<template>
  <Layout>
    <LayoutSider v-model:collapsed="collapsed" :trigger="null" collapsible>
      <div class="logo">
        <h1 style="padding: 5px  30px; font-weight: 900; font-size:x-large; color:rgb(2, 133, 133)">
          Big Data
        </h1>
      </div>
      <Menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <MenuItem key="1">
          <UserOutlined />
          <span>Trending</span>
        </MenuItem>
        <MenuItem key="2">
          <UserOutlined />
          <span>Top trending</span>
        </MenuItem>
        <MenuItem key="3">
          <UserOutlined />
          <span>Charts</span>
        </MenuItem>
        <MenuItem key="4">
          <UserOutlined />
          <span>Correlations</span>
        </MenuItem>
      </Menu>
    </LayoutSider>
    <Layout>
      <LayoutHeader style="background: #fff; padding: 0">
        <MenuUnfoldOutlined
          v-if="collapsed"
          class="trigger"
          @click="() => (collapsed = !collapsed)"
        />
        <MenuFoldOutlined v-else class="trigger" @click="() => (collapsed = !collapsed)" />
      </LayoutHeader>
      <LayoutContent
        :style="{ margin: '24px 16px', padding: '24px', background: '#fff', minHeight: '280px' }"
      >
        <Charts v-if="selectedKeys == 3"/>
        <Correlations  v-if="selectedKeys == 4"/>
        <Trending  v-if="selectedKeys == 1"/>
        <TopTrending  v-if="selectedKeys == 2"/>
      </LayoutContent>
    </Layout>
  </Layout>
</template>

<script>
import { ref } from 'vue';
const selectedKeys = ref(['1']);
const collapsed = ref(false);
</script>

<style scoped>
#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.3);
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}
</style>
