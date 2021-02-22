<template>
  <div style="margin: 0 24px">
    <div style="padding: 24px 0">
      <h2 style="float: left">留言订单</h2>
      <!--<ButtonGroup style="float: right">
        <Button @click="importOrders">导出数据</Button>
        <Input style="width: 200px; margin-left: 20px" search />
      </ButtonGroup>-->
    </div>
    <Divider />
    <IntentionsTable></IntentionsTable>
  </div>
</template>

<script>
import IntentionsTable from '@/components/IntentionsTable'

export default {
  name: 'IntentionsListView',
  components: {
    IntentionsTable
  },
  data () {
    return {}
  },
  methods: {}
}
</script>

<style></style>
