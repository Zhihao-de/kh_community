<template>
  <div style="margin: 0 24px">
    <div style="padding: 24px 0">
      <h2 style="float: left">商品类别</h2>
      <ButtonGroup style="float: right">
        <Button @click="openEditor(null)">新增类别</Button>
      </ButtonGroup>
    </div>
    <Divider />
    <Table
      :data="categories"
      :columns="categoryFields"
      :loading="dataLoading"
      stripe
      border
    >
    </Table>
    <Modal
      title="编辑商品类别"
      v-model="showCategoryEditor"
      :footer-hide="true"
    >
      <Form
        ref="form"
        :model="currentCategory"
        :label-width="80"
        :rules="validators"
      >
        <FormItem label="类别名称" prop="name">
          <Input
            v-model="currentCategory.name"
            placeholder="请输入类别名称..."
            clearable
          />
        </FormItem>
        <FormItem label="显示顺序" prop="order">
          <Input v-model="currentCategory.order" number clearable />
        </FormItem>
        <FormItem label="类别描述">
          <Input
            v-model="currentCategory.description"
            placeholder="请输入类别描述..."
            clearable
          />
        </FormItem>
        <FormItem label="类别图片">
          <ImageUpload
            :limit="1"
            v-model="currentCategory.pic_url"
          ></ImageUpload>
        </FormItem>
        <FormItem label="父级ID">
          <Input v-model="currentCategory.parent" number clearable />
        </FormItem>

        <!-- 提交 -->
        <div style="text-align: center">
          <Button
            type="primary"
            size="large"
            style="width: 120px"
            :loading="asyncHandling"
            @click="confirmSubmit()"
            >提交</Button
          >
        </div>
      </Form>
    </Modal>
  </div>
</template>

<script>
import {
  listProductCategories,
  postOrPatchProductCategory,
  defaultProductCategoryModel
} from '@/api/product_api'
import ImageUpload from '@/components/ImageUpload'

export default {
  name: 'ProductCategoryEditView',
  components: { ImageUpload },
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      asyncHandling: false,

      /* 商品分类列表 */
      categories: [],

      currentCategory: defaultProductCategoryModel(),
      showCategoryEditor: false,

      validators: {
        name: [
          { required: true, message: '类别名称不能为空', trigger: 'blur' }
        ],
        order: [
          {
            required: true,
            type: 'number',
            message: '显示顺序应为数字且不为空',
            trigger: 'blur'
          }
        ]
      },

      /* 产品分类列表的字段定义 */
      categoryFields: [
        {
          title: 'ID',
          key: 'id',
          align: 'center',
          width: 80,
          resizable: true
        },
        {
          title: '父ID',
          key: 'parent',
          align: 'center',
          width: 80,
          resizable: true
        },
        {
          title: '类别图片',
          align: 'center',
          width: 120,
          resizable: true,
          render: (h, params) => {
            return h('img', {
              attrs: {
                src: params.row.pic_url[0].split(',')[1]
              },
              style: {
                width: '64px',
                height: '64px'
              }
            })
          }
        },
        {
          title: '类别名称',
          key: 'name',
          align: 'center',
          width: 160,
          resizable: true
        },
        {
          title: '类别描述',
          key: 'description',
          align: 'center',
          minWidth: 200,
          resizable: true
        },
        {
          title: '显示顺序',
          key: 'order',
          align: 'center',
          width: 120,
          resizable: true
        },
        {
          title: '创建时间',
          key: 'created_at',
          align: 'center',
          width: 120,
          resizable: true
        },
        {
          title: '操作',
          fixed: 'right',
          align: 'center',
          width: 120,
          resizable: true,
          render: (h, params) => {
            return h(
              'Button',
              {
                props: {
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  // click事件进行跳转
                  click: () => {
                    this.openEditor(params.row)
                  }
                }
              },
              '编辑'
            )
          }
        }
      ]
    }
  },
  created () {
    this.getProductCategories()
  },
  methods: {
    openEditor (category) {
      this.currentCategory = category || defaultProductCategoryModel()
      this.showCategoryEditor = true
    },
    getProductCategories () {
      this.dataLoading = true
      listProductCategories()
        .then(res => {
          this.categories = res.data
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.dataLoading = false
        })
    },
    confirmSubmit () {
      this.asyncHandling = true
      this.$refs.form.validate(valid => {
        if (valid) {
          this.$Modal.confirm({
            title: '操作确认',
            content: '确定提交商品类别信息？',
            onOk: () => {
              this.submit()
            },
            onCancel: () => {
              this.asyncHandling = false
            }
          })
        } else {
          this.asyncHandling = false
          this.$Notice.error({
            title: '商品类别信息有误',
            desc: '一个或多个商品类别信息不正确，请修改后重试。'
          })
        }
      })
    },
    submit () {
      postOrPatchProductCategory(this.currentCategory)
        .then(resp => {
          if (resp.config.method === 'post') {
            this.categories.push(resp.data)
          }
          this.$Message.info('操作成功！')
          this.asyncHandling = false
          this.showCategoryEditor = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.asyncHandling = false
        })
    }
  }
}
</script>

<style scoped></style>
