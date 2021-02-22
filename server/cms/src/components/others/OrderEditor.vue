<template>
  <Form ref="OrderForm" :model="model" :rules="productRules" :label-width="80">
    <FormItem label="留言订单" prop="intention">
      <Input v-model="model.intention" placeholder="请输入留言订单号..." />
    </FormItem>
    <FormItem label="品名" prop="total">
      <Input v-model="model.total" placeholder="请输入总量..." />
    </FormItem>
    <FormItem label="副标题" prop="title">
      <Input v-model="model.title" placeholder="请输入副标题..." />
    </FormItem>

    <div style="text-align: center">
      <Button
        type="primary"
        size="large"
        style="width: 120px"
        :loading="asyncHandling"
        @click="submit()"
        >提交
      </Button>
    </div>
  </Form>
</template>

<script>
import { defaultOrder, postOrPatchOrder } from "@/api/order_api";

/**
 * 产品模型编辑器组件
 * 事件：on-ok 提交成功后触发
 */
export default {
  name: "OrderEditor",
  props: {
    /*订单模型*/
    model: {
      type: Object,
      default: defaultOrder()
    }
  },
  data() {
    return {
      /*产品属性值验证规则*/
      productRules: {
        intention: [
          { required: true, message: "留言订单不能为空", trigger: "blur" }
        ],
        name: [{ required: true, message: "品名不能为空", trigger: "blur" }],
        title: [{ required: true, message: "副标题不能为空", trigger: "blur" }]
      },

      /*是否显示图像查看器对话框*/
      showViewer: false,

      /*是否正在异步提交*/
      asyncHandling: false
    };
  },
  watch: {
    /*属性值变更通知*/
  },
  methods: {
    /**
     * 提交表单
     * @returns {*}
     */
    submit() {
      var model = this.$props["model"];
      this.$refs["OrderForm"].validate(valid => {
        if (valid) {
          this.asyncHandling = true;

          this.$Modal.confirm({
            title: "操作确认",
            content: "确定提交产品信息？",
            onOk: () => {
              // 新建或更新产品模型
              postOrPatchOrder(model)
                .then(() => {
                  this.$Message.info("操作成功！");
                  this.asyncHandling = false;
                  this.$emit("on-ok");
                })
                .catch(err => {
                  this.$Message.error(err);
                  this.asyncHandling = false;
                });
            },
            onCancel: () => {
              this.asyncHandling = false;
            }
          });
        } else {
          this.$Notice.error({
            title: "产品信息有误",
            desc: "订单不正确，请修改后重试。"
          });
        }
      });
    }
  },
  mounted() {}
};
</script>

<style scoped>
.number-input {
  width: 130px;
  margin-right: 5px;
}

.upload-images-list {
  display: inline-block;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  border: 1px solid transparent;
  border-radius: 4px;
  overflow: hidden;
  background: #fff;
  position: relative;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  margin-right: 4px;
}

.upload-images-list img {
  width: 100%;
  height: 100%;
}

.upload-images-list-cover {
  display: none;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
}

.upload-images-list:hover .upload-images-list-cover {
  display: block;
}

.upload-images-list-cover i {
  color: #fff;
  font-size: 20px;
  cursor: pointer;
  margin: 0 2px;
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
