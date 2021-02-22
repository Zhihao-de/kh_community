<template>
  <div>
    <div style="padding: 20px; margin-left:20px; margin-bottom: 20px">
      <div style="margin-top: 8px">
        <div style="float: left">
          <img
            width="64"
            height="64"
            style="margin-right: 16px"
            :src="this.$route.params.user.wx_avatar_url"
          />
        </div>
        <div>
          <h3>{{ this.$route.params.user.wx_name }}</h3>
          <div style="color: dimgrey">{{ this.$route.params.user.mobile }}</div>
        </div>
      </div>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>申请记录</strong></p>
        <UserApplicationsTable></UserApplicationsTable>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>地图定位</strong></p>
        <UserLocationEditor></UserLocationEditor>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>产品价格表</strong></p>
        <Upload
          :before-upload="handleUpload"
          action="//jsonplaceholder.typicode.com/posts/"
        >
          <Button icon="ios-cloud-upload-outline">选择价格表文件...</Button>
        </Upload>
        <div v-if="file !== null">价格表文件: {{ file.name }}</div>
        <UserDocsTable></UserDocsTable>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>运费价格表</strong></p>
        <Upload
          :before-upload="handleUpload"
          action="//jsonplaceholder.typicode.com/posts/"
        >
          <Button icon="ios-cloud-upload-outline">选择运费表文件...</Button>
        </Upload>
        <div v-if="file !== null">运费表文件: {{ file.name }}</div>
        <UserDocsTable></UserDocsTable>
      </Card>
    </div>
  </div>
</template>

<script>
import UserDocsTable from '@/components/UserDocsTable'
import UserLocationEditor from '@/components/UserLocationEditor'
import UserApplicationsTable from '@/components/UserApplicationsTable'

export default {
  name: 'UserDetailView',
  components: {
    UserApplicationsTable,
    UserLocationEditor,
    UserDocsTable
  },
  data () {
    return {
      file: null
    }
  },
  methods: {
    handleUpload (file) {
      this.file = file
      return false
    }
  }
}
</script>

<style></style>
