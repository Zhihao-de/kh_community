<template>
  <div class="layout">
    <Layout>
      <Header class="layout-header">
        <Menu mode="horizontal" theme="dark">
          <div class="layout-logo"></div>
          <div class="layout-nav">
            <a href="/cms" target="_blank">
              <MenuItem name="cms">
              <Icon type="ios-paper" size="20"></Icon>
              社区CMS管理
              </MenuItem>
            </a>
            <MenuItem name="mmi-logout" to="/logout">
            <Icon type="ios-exit" size="20"></Icon>
            登出
            </MenuItem>
          </div>
        </Menu>
      </Header>
      <Layout>
        <Sider hide-trigger class="layout-sider ">
          <Menu theme="dark" width="auto" :open-names="['root']" active-name="products_list">
            <Submenu name="root">
              <template slot="title">
                <Icon type="ios-navigate"></Icon>
                业务管理
              </template>
              <MenuItem name="products_list" to="/products">商品管理</MenuItem>
              <MenuItem name="orders_list" to="/orders">商品订单管理</MenuItem>
              <MenuItem name="intentions_list" to="/intentions">留言订单管理
              </MenuItem>
              <MenuItem name="users_list" to="/users">用户管理</MenuItem>
            </Submenu>
          </Menu>
        </Sider>
        <Layout :style="{ padding: 0, marginLeft: '200px', marginTop: '0px' }">
          <Header class="layout-content-header">
            <Breadcrumb :style="{ margin: '0 24px' }">
              <BreadcrumbItem>首页</BreadcrumbItem>
              <BreadcrumbItem v-for="(item, index) in $route.meta.name" :key="index">
                {{ item }}
              </BreadcrumbItem>
            </Breadcrumb>
          </Header>
          <Content class="layout-content" :style="{ marginTop: '60px' }">
            <router-view></router-view>
          </Content>
          <Footer class="layout-content-footer">
            2020-2021 &copy; 开皇社区业务管理系统
          </Footer>
        </Layout>
      </Layout>
    </Layout>
  </div>
</template>

<script>
export default {
  name: 'Home',
  components: {},
  methods: {
    onMainMenuItemSelect (name) {
      if (name.equal('cms')) {}
    }
  }
}
</script>

<style scoped>
  .layout {
    background: #f5f7f9;
    position: relative;
    min-height: 100vh;
    overflow: hidden;
  }

  .layout-logo {
    width: 100px;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    float: left;
    position: relative;
    top: 15px;
    left: 20px;
  }

  .layout-nav {
    width: 420px;
    margin: 0 auto;
    margin-right: 20px;
  }

  .layout-header {
    position: fixed;
    top:0px;
    width: 100%;
    z-index: 100;
  }

  .layout-sider {
    background: #363e4f;
    position: fixed;
    height: 100vh;
    left: 0;
    top: 64px;
    overflow: auto;
  }

  .layout-content-header {
    position: fixed;
    width: 100%;
    background: #f5f7f9;
    padding: 0;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
    z-index: 100;
  }

  .layout-content {
    padding: 24px;
    background: #fff;
    margin: 0 24px;
  }

  .layout-content-footer {
    text-align: center;
  }
</style>
