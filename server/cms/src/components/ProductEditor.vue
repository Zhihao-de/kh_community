<template>
  <Form
    ref="form"
    :model="currentProduct"
    :rules="validators"
    :label-width="80"
  >
    <!-- 基本信息 -->
  <div style="padding: 20px">
    <Card :bordered="false">
    <p slot="title"><strong>基本信息</strong></p>
   <FormItem label="商品类别">
   <Tag
      color="success"
      size="medium"
      v-for="(item, index) in this.$route.params.categoryPath.split('/')"
      :key="index"
   >{{ item }}</Tag>
   </FormItem>
<FormItem label="品名" prop="name">
<Input v-model="currentProduct.name" placeholder="请输入产品名称..." />
</FormItem>
<FormItem label="副标题">
<Input v-model="currentProduct.title" placeholder="请输入产品副标题..." />
</FormItem>
<FormItem label="产品图片">
<ImageUpload :limit="1" v-model="currentProduct.pic_url"></ImageUpload>
</FormItem>
</Card>
</div>

    <!-- 重量、价格和库存 -->
<div style="padding: 20px">
<Card :bordered="false">
<p slot="title"><strong>重量、价格和库存</strong></p>
<div style="display: flex;">
<FormItem label="重量">
       <InputNumber
         :max="1000000"
         :min="0"
         :step="1.0"
         v-model="currentProduct.weight"
         class="number-input"
       ></InputNumber>
     </FormItem>
     <FormItem label="单位">
       <Select v-model="currentProduct.unit" class="number-input">
         <Option value="克">克</Option>
         <Option value="克/盒">克/盒</Option>
         <Option value="克/单果">克/单果</Option>
         <Option value="千克">千克</Option>
         <Option value="斤">斤</Option>
         <Option value="斤/单果">斤/单果</Option>
         <Option value="公斤">公斤</Option>
          <Option value="磅">磅</Option>
         <Option value="盎司">盎司</Option>
       </Select>
     </FormItem>
   </div>
   <div style="display: flex;">
     <FormItem label="采购价(元)">
       <InputNumber
         :max="1000000"
         :min="0"
         :step="1.0"
         v-model="currentProduct.purchase_price"
         class="number-input"
       ></InputNumber>
     </FormItem>
     <FormItem label="指导价(元)">
       <InputNumber
         :max="1000000"
            :min="0"
         :step="1.0"
         v-model="currentProduct.retail_price"
         class="number-input"
       ></InputNumber>
     </FormItem>
   </div>
   <FormItem label="库存">
     <InputNumber
       :max="100000"
       :min="0"
       :step="1"
       v-model="currentProduct.stock"
       class="number-input"
     ></InputNumber>
    </FormItem>
 </Card>
</div>

    <!-- 产品介绍 -->
<div style="padding: 20px">
 <Card :bordered="false">
   <p slot="title"><strong>产品介绍</strong></p>
   <FormItem label="轮播图片">
     <ImageUpload
       :limit="4"
       v-model="currentProduct.carousal_urls"
     ></ImageUpload>
   </FormItem>
   <FormItem label="产品描述">
     <quill-editor
       :options="editorOption"
       v-model="currentProduct.description"
     ></quill-editor>
   </FormItem>
 </Card>
    </div>

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
</template>

<script>
import { postOrPatchProductModel } from '@/api/product_api'
// import ProductCategoryEditor from "@/components/ProductCategoryEditor";
import ImageUpload from '@/components/ImageUpload'

/**
 * 产品模型编辑器组件
 * 事件：on-ok 提交成功后触发
 */
export default {
  name: 'ProductEditor',
  components: { ImageUpload },
  data () {
    return {
      currentProduct: this.$route.params.model,

      /* 是否正在异步提交 */
      asyncHandling: false,

      /* 产品属性值验证规则 */
      validators: {
        name: [{ required: true, message: '产品名称不能为空', trigger: 'blur' }]
      },

      /* 富文本编辑器选项设置 */
      editorOption: {
        placeholder: '请输入产品描述...',
        modules: {
          toolbar: [
            ['bold', 'italic', 'underline', 'strike'], // 加粗，斜体，下划线，删除线
            ['blockquote'], // 引用

            [{ header: 1 }, { header: 2 }], // 标题，键值对的形式；1、2表示字体大小
            [{ list: 'ordered' }, { list: 'bullet' }], // 列表
            [{ script: 'sub' }, { script: 'super' }], // 上下标
            [{ indent: '-1' }, { indent: '+1' }], // 缩进
            [{ size: ['small', false, 'large', 'huge'] }], // 字体大小
            [{ header: [1, 2, 3, 4, 5, 6, false] }], // 标题级别

            [{ color: [] }, { background: [] }], // 字体颜色，字体背景颜色
            [{ font: [] }], // 字体
            [{ align: [] }], // 对齐方式
            ['clean'], // 清除字体样式
            ['link', 'image', 'video'] // 上传图片、上传视频
          ]
        },
        theme: 'snow'
      },

      showCategoryEditor: false
    }
  },
  methods: {
    editProductCategory () {
      this.showCategoryEditor = true
    },
    /**
     * 确认提交表单
     * @returns {*}
     */
    confirmSubmit () {
      this.asyncHandling = true
      this.$refs.form.validate(valid => {
        if (valid) {
          this.$Modal.confirm({
            title: '操作确认',
            content: '确定提交商品信息？',
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
            title: '商品信息有误',
            desc: '一个或多个商品信息不正确，请修改后重试。'
          })
        }
      })
    },
    /**
     * 提交表单
     * @returns {*}
     */
    submit () {
      postOrPatchProductModel(this.currentProduct)
        .then(() => {
          this.$Message.info('操作成功！')
          this.asyncHandling = false
          this.$emit('on-ok')
        })
        .catch(err => {
          this.$Message.error(err)
          this.asyncHandling = false
        })
    }
  }
}
</script>

<style scoped>
.number-input {
  width: 130px;
  margin-right: 5px;
}
</style>

<style>
.ql-editor {
  height: 400px;
}

.ql-snow .ql-picker.ql-size .ql-picker-label::before,
.ql-snow .ql-picker.ql-size .ql-picker-item::before {
  content: "14px";
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="small"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="small"]::before {
  content: "10px";
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="large"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="large"]::before {
  content: "18px";
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="huge"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="huge"]::before {
  content: "32px";
}

.ql-snow .ql-picker.ql-header .ql-picker-label::before,
.ql-snow .ql-picker.ql-header .ql-picker-item::before {
  content: "文本";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="1"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
  content: "标题1";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="2"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
  content: "标题2";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
  content: "标题3";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="4"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
  content: "标题4";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
  content: "标题5";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="6"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
  content: "标题6";
}

.ql-snow .ql-picker.ql-font .ql-picker-label::before,
.ql-snow .ql-picker.ql-font .ql-picker-item::before {
  content: "标准字体";
}
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="serif"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="serif"]::before {
  content: "衬线字体";
}
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="monospace"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="monospace"]::before {
  content: "等宽字体";
}
</style>
