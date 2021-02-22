<template>
  <div style="margin: 0 24px">
    <div style="padding: 24px 0">
      <h2 style="float: left">用户</h2>
      <ButtonGroup style="float: right">
        <Input style="width: 200px; margin-left: 20px" search />
      </ButtonGroup>
    </div>
    <Divider />
    <UsersTable></UsersTable>
  </div>
</template>

<script>
import UsersTable from '@/components/UsersTable'

export default {
  name: 'UsersListView',
  components: {
    UsersTable
  },
  data () {
    return {}
  },
  methods: {}
}
</script>

<style></style>
