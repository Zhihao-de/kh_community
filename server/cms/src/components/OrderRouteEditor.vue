<template>
  <Form ref="orderRouteForm" :rules="rules" :model="model" :label-width="100">
    <FormItem label="物流公司" prop="express">
      <Select v-model="model.express" style="width:200px">
        <Option
          v-for="item in expressList"
          :value="item.value"
          :key="item.value"
          >{{ item.label }}</Option
        >
      </Select>
    </FormItem>
    <FormItem label="物流单号" prop="receipt_no">
      <Input v-model="model.receipt_no" placeholder="请输入物流单号..." />
    </FormItem>
    <FormItem label="收件人信息" prop="route_info">
      <Input
        v-model="model.address"
        placeholder="请输入收件人姓名,联系方式,地址等信息..."
      />
    </FormItem>
    <FormItem label="数量(件)">
      <InputNumber
        :max="1000000"
        :min="1"
        :step="1"
        v-model="model.quantity"
        class="number-input"
      ></InputNumber>
    </FormItem>
    <FormItem label="总重(千克)">
      <InputNumber
        :max="1000000"
        :min="0"
        :step="1.0"
        v-model="model.weight"
        class="number-input"
      ></InputNumber>
    </FormItem>
    <FormItem label="运费(元)">
      <InputNumber
        :max="1000000"
        :min="0"
        :step="1.0"
        v-model="model.cost"
        class="number-input"
      ></InputNumber>
    </FormItem>
    <FormItem label="运费(元)">
      <Input
        v-model="model.remark"
        type="textarea"
        :rows="4"
        placeholder="请输入备注信息,如物品名称和规格等..."
      />
    </FormItem>
    <!-- 提交 -->
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
import { defaultOrderRoute, postOrPatchOrderRoute } from '@/api/order_api'
export default {
  name: 'OrderRouteEditor',
  props: {
    // 订单物流对象
    model: {
      type: Object,
      default: defaultOrderRoute()
    }
  },
  data () {
    return {
      expressList: [
        {
          value: '顺丰',
          label: '顺丰'
        },
        {
          value: '圆通',
          label: '圆通'
        },
        {
          value: '申通',
          label: '申通'
        },
        {
          value: '韵达',
          label: '韵达'
        },
        {
          value: '中通',
          label: '中通'
        },
        {
          value: 'EMS',
          label: 'EMS'
        },
        {
          value: '宅急送',
          label: '宅急送'
        },
        {
          value: '全峰',
          label: '全峰'
        },
        {
          value: '优速',
          label: '优速'
        },
        {
          value: '如风达',
          label: '如风达'
        },
        {
          value: '邮政包裹',
          label: '邮政包裹'
        }
      ],

      /* 是否正在异步提交 */
      asyncHandling: false,

      /* 验证当前的配送订单号规则 */
      rules: {
        express: [
          { required: true, message: '物流公司不能为空', trigger: 'blur' }
        ],
        receipt_no: [
          { required: true, message: '物流单号不能为空', trigger: 'blur' }
        ]
      },

      dataLoading: false,

      orderDetails: [],

      /* 商品订单列表的字段定义 */
      orderDetailFields: [
        {
          type: 'selection',
          width: 60,
          align: 'center'
        },
        {
          title: '商品名称',
          key: 'product_name',
          minWidth: 300,
          resizable: true
        },
        {
          title: '重量',
          align: 'center',
          width: 120,
          resizable: true,
          render: (h, params) => {
            return h(
              'span',
              params.row.product_weight + params.row.product_unit
            )
          }
        },
        {
          title: '数量(件)',
          key: 'quantity',
          align: 'center',
          width: 90,
          resizable: true
        },
        {
          title: '价格(元)',
          key: 'purchase_price',
          align: 'center',
          width: 90,
          resizable: true
        },
        {
          title: '总价(元)',
          key: 'total_price',
          align: 'center',
          width: 90,
          resizable: true
        }
      ]
    }
  },
  created () {},
  methods: {
    /**
     * 确认提交表单
     * @returns {*}
     */
    confirmSubmit () {
      this.asyncHandling = true
      this.$Modal.confirm({
        title: '操作确认',
        content: '确定提交物流信息？',
        onOk: () => {
          this.submit()
        },
        onCancel: () => {
          this.asyncHandling = false
        }
      })
    },
    /**
     * 提交表单
     * @returns {*}
     */
    submit () {
      this.$refs.orderRouteForm.validate(valid => {
        if (valid) {
          postOrPatchOrderRoute(this.model)
            .then(() => {
              this.$Message.info('操作成功！')
              this.asyncHandling = false
              this.$emit('on-update')
            })
            .catch(err => {
              this.$Message.error(err.toString())
              this.asyncHandling = false
            })
        } else {
          this.$Notice.error({
            title: '物流信息有误',
            desc: '商品订单的物流信息有错误，请修改后重试。'
          })
        }
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
