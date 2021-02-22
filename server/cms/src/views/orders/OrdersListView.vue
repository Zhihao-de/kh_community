<template>
  <div style="margin: 0 24px">
    <div style="padding: 24px 0">
      <h2 style="float: left">商品订单</h2>
      <ButtonGroup style="float: right">
        <Button>导出数据</Button>
        <Input style="width: 200px; margin-left: 20px" search />
      </ButtonGroup>
    </div>
    <Divider />
    <OrdersTable></OrdersTable>
  </div>
</template>

<script>
import OrdersTable from '@/components/OrdersTable'

export default {
  name: 'OrdersListView',
  components: {
    OrdersTable
  },
  data () {
    return {}
  },
  methods: {}
}
</script>
<style></style>
