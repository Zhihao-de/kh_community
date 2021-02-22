<template>
  <div style="margin: 0 24px">
    <div style="padding: 24px 0">
      <h2 style="float: left">商品</h2>
      <ButtonGroup style="float: right">
        <Button @click="openProductCategoryEditor">编辑分类</Button>
        <Button @click="openProductEditor">新增商品</Button>
        <Input style="width: 200px; margin-left: 20px" search />
      </ButtonGroup>
    </div>
    <Divider />
    <Layout>
      <Content :style="{ minHeight: '280px', background: '#fff' }">
        <Layout>
          <Sider hide-trigger :style="{ background: '#fff' }">
            <Menu
              theme="light"
              width="auto"
              :open-names="['root']"
              @on-select="onCategorySelected"
            >
              <Submenu
                name="root"
                :open-names="
                  productCategories.map(c => {
                    return c.id;
                  })
                "
              >
                <template slot="title">
                  <Icon type="md-menu"></Icon>
                  商品分类
                </template>
                <Submenu
                  :name="c.id"
                  v-for="c in productCategories"
                  :key="c.id"
                >
                  <template slot="title">
                    <Icon type="ios-flower"></Icon>
                    {{ c.name }}
                  </template>
                  <MenuItem
                    :name="c.id + '-' + c.name + '/' + cc.id + '-' + cc.name"
                    v-for="cc in c.children"
                    :key="cc.id"
                  >
                    {{ cc.name }}
                  </MenuItem>
                </Submenu>
              </Submenu>
            </Menu>
          </Sider>
          <Content
            :style="{
              padding: '0 0 0 24px',
              minHeight: '280px',
              background: '#fff'
            }"
          >
            <ProductsTable :categoryPath="selectedCategoryPath"></ProductsTable>
          </Content>
        </Layout>
      </Content>
    </Layout>
  </div>
</template>

<script>
import {
  listProductCategoryTree,
  defaultProductModel
} from '@/api/product_api'
import ProductsTable from '@/components/ProductsTable'
export default {
  name: 'ProductsListView',
  components: {
    ProductsTable
  },
  created () {
    this.getProductCategories()
  },
  data () {
    return {
      selectedCategoryPath: '',
      productCategories: []
    }
  },
  methods: {
    getProductCategories () {
      listProductCategoryTree()
        .then(res => {
          this.productCategories = res.status === 200 ? res.data : []
        })
        .catch(err => {
          this.$Message.error(err)
        })
    },
    openProductCategoryEditor () {
      this.$router.push({
        name: 'product_category_edit',
        params: {}
      })
    },
    openProductEditor () {
      if (!this.selectedCategoryPath) {
        this.$Message.error('请选择一种产品类别！')
        return
      }
      const p = this.selectedCategoryPath.split('/')
      const categoryId = p[p.length - 1].split('-')[0]
      this.$router.push({
        name: 'product_add',
        params: {
          categoryPath: this.selectedCategoryPath,
          model: defaultProductModel(categoryId)
        }
      })
    },
    onCategorySelected (path) {
      this.selectedCategoryPath = path
    }
  }
}
</script>

<style>
.number-input {
  width: 130px;
  margin-right: 5px;
}
</style>
