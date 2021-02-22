<template>
  <div>
    <Table
      :data="productsList"
      :columns="productFields"
      :loading="dataLoading"
      stripe
      border
    ></Table>
    <div style="margin: 10px; overflow: hidden">
      <div style="float: right;">
        <Page
          :page-size="4"
          :total="count"
          :current="1"
          @on-change="onPageChanged"
        ></Page>
      </div>
    </div>
  </div>
</template>

<script>
import {
  listProducts,
  patchProductModelByFlags,
  splitImageUrls
} from '@/api/product_api'

/**
 * 产品模型列表
 */
export default {
  name: 'ProductsTable',
  props: {
    /* 类别路径 */
    categoryPath: String
  },
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      categoryId: 0,

      /* 产品总数，用于设置分页器 */
      count: 0,

      /* 产品模型列表 */
      productsList: [],

      /* 产品列表的字段定义 */
      productFields: [
        {
          type: 'index',
          align: 'center',
          width: 60,
          resizable: true
        },
        {
          title: '品名',
          key: 'name',
          minWidth: 200,
          resizable: true
        },
        {
          title: '重量',
          key: 'weight',
          align: 'center',
          width: 100,
          resizable: true
        },
        {
          title: '单位',
          key: 'unit',
          align: 'center',
          width: 100,
          resizable: true
        },
        {
          title: '采购价',
          key: 'purchase_price',
          align: 'center',
          width: 100,
          resizable: true
        },
        {
          title: '指导价',
          key: 'retail_price',
          align: 'center',
          width: 100,
          resizable: true
        },
        {
          title: '库存',
          key: 'stock',
          align: 'center',
          width: 100,
          resizable: true
        },
        {
          title: '状态',
          key: 'flags',
          align: 'center',
          width: 120,
          sortable: true,
          resizable: true,
          render: (h, params) => {
            return h(
              'Tag',
              {
                props: {
                  type: 'dot',
                  color: this.getFlagsColor(params.row.flags)
                }
              },
              this.getFlagsText(params.row.flags)
            )
          }
        },
        {
          title: '操作',
          key: 'action',
          width: 146,
          align: 'center',
          fixed: 'right',
          resizable: true,
          render: (h, params) => {
            if (
              params.row.flags === 0 /* 在售 */ ||
              params.row.flags === 3 /* 作废 */
            ) {
              return h(
                'Button',
                {
                  props: {
                    type: 'warning',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px',
                    paddingTop: '5px',
                    paddingLeft: '10px',
                    paddingRight: '10px',
                    paddingBottom: '25px'
                  },
                  on: {
                    click: () => {
                      this.updateProductModelByFlags(params.row, 1)
                    }
                  }
                },
                '售罄'
              )
            } else if (params.row.flags === 2 /* 编辑 */) {
              return h('div', [
                h(
                  'Button',
                  {
                    props: {
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px',
                      paddingTop: '5px',
                      paddingLeft: '10px',
                      paddingRight: '10px',
                      paddingBottom: '25px'
                    },
                    on: {
                      click: () => {
                        console.log(params.row)
                        this.showProductEditor(params.row)
                      }
                    }
                  },
                  '修改'
                ),
                h(
                  'Button',
                  {
                    props: {
                      type: 'success',
                      size: 'small'
                    },
                    style: {
                      paddingTop: '5px',
                      paddingLeft: '10px',
                      paddingRight: '10px',
                      paddingBottom: '25px'
                    },
                    on: {
                      click: () => {
                        this.updateProductModelByFlags(params.row, 0)
                      }
                    }
                  },
                  '在售'
                )
              ])
            } else {
              return h('div', [
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px',
                      paddingTop: '5px',
                      paddingLeft: '10px',
                      paddingRight: '10px',
                      paddingBottom: '25px'
                    },
                    on: {
                      click: () => {
                        this.updateProductModelByFlags(params.row, 2)
                      }
                    }
                  },
                  '编辑'
                ),
                h(
                  'Button',
                  {
                    props: {
                      type: 'error',
                      size: 'small'
                    },
                    style: {
                      paddingTop: '5px',
                      paddingLeft: '10px',
                      paddingRight: '10px',
                      paddingBottom: '25px'
                    },
                    on: {
                      click: () => {
                        this.updateProductModelByFlags(params.row, 3)
                      }
                    }
                  },
                  '作废'
                )
              ])
            }
          }
        }
      ]
    }
  },
  watch: {
    categoryPath: {
      immediate: true, // 这句重要
      handler (val) {
        if (!val) return
        const p = val.split('/')
        this.categoryId = p[p.length - 1].split('-')[0]
        //
        // 初始化产品模型列表
        this.dataLoading = true
        listProducts(this.categoryId, 1)
          .then(res => {
            this.productsList = res.data.results
            this.count = res.data.count
            this.dataLoading = false
          })
          .catch(err => {
            this.$Message.error(err)
            this.dataLoading = false
          })
      }
    }
  },
  created () {},
  methods: {
    /**
     * 获取产品状态的名称
     * @param flags 产品状态
     * @returns {*}
     */
    getFlagsText (flags) {
      return flags === 0
        ? '在售'
        : flags === 1
          ? '售罄'
          : flags === 2
            ? '编辑'
            : '作废'
    },
    /**
     * 获取产品状态的颜色
     * @param flags 产品状态
     * @returns {*}
     */
    getFlagsColor (flags) {
      return flags === 0
        ? '#19be6b' /* success */
        : flags === 1
          ? '#ff9900' /* warning */
          : flags === 2
            ? '#2d8cf0' /* primary */
            : '#ed4014' /* error */
    },
    /**
     * 更新产品状态
     * @param productModel 当前产品模型
     * @param flags 产品状态
     * @returns {*}
     */
    updateProductModelByFlags (productModel, flags) {
      const oldFlagsColor = this.getFlagsColor(productModel.flags)
      const newFlagsColor = this.getFlagsColor(flags)
      this.$Modal.confirm({
        title: '操作确认',
        content:
          '确定将产品 <strong>' +
          productModel.name +
          "</strong> 的状态从 <font color='" +
          oldFlagsColor +
          "'>" +
          this.getFlagsText(productModel.flags) +
          "</font> 转变为 <font color='" +
          newFlagsColor +
          "'>" +
          this.getFlagsText(flags) +
          '</font> ？',
        onOk: () => {
          this.dataLoading = true
          patchProductModelByFlags(productModel.id, flags)
            .then(() => {
              productModel.flags = flags
              this.$Message.info('操作成功！')
              this.dataLoading = false
            })
            .catch(err => {
              this.$Message.error(err)
              this.dataLoading = false
            })
        }
      })
    },
    doSplitImageUrls (imageUrls) {
      return splitImageUrls(imageUrls)
    },
    /**
     * 显示产品模型编辑器
     * @param productModel 当前产品模型
     * @returns {*}
     */
    showProductEditor (productModel) {
      this.$router.push({
        name: 'product_edit',
        params: {
          categoryPath: this.categoryPath,
          model: productModel
        }
      })
    },
    /**
     * 换页的事件处理
     * @param page 页索引
     * @returns {*}
     */
    onPageChanged (page) {
      this.dataLoading = true
      listProducts(this.categoryId, page)
        .then(res => {
          this.productsList = res.data.results
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err)
          this.dataLoading = false
        })
    }
  }
}
</script>

<style scoped>
.model-viewer-description-center {
  display: block;
  width: 800px;
  margin: 0 auto;
  overflow: auto;
}
</style>
