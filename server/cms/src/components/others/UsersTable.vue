<template>
  <div>
    <Table
      :data="UsersList"
      :columns="UserFields"
      :loading="dataLoading"
      stripe
      border
    ></Table>
    <div style="margin: 10px;overflow: hidden">
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
import { listUserModels } from "@/api/user_api";

/**
 * 产品用户列表
 */
export default {
  name: "UsersTable",
  data() {
    return {
      /*是否正在拉取列表数据*/
      dataLoading: false,

      /*产品总数，用于设置分页器*/
      count: 0,

      /*产品模型列表*/
      UsersList: [],

      /*是否显示产品介绍查看器*/
      showModelViewer: false,

      /*产品列表的字段定义*/
      UserFields: [
        {
          type: "index",
          align: "center",
          width: 60,
          resizable: true
        },
        {
          title: "微信号",
          key: "wx_open_id",
          width: 100,
          resizable: true
        },
        {
          title: "微信名",
          key: "wx_name",
          width: 100,
          resizable: true
        },
        {
          title: "手机号码",
          key: "phone",

          resizable: true
        },
        {
          title: "Proxy",
          key: "is_proxy",
          width: 100,
          resizable: true
        },
        {
          title: "email",
          key: "email",

          resizable: true
        }
      ]
    };
  },
  created() {
    // 初始化产品模型列表
    this.dataLoading = true;
    listUserModels(1)
      .then(res => {
        this.UsersList = res.data.results;
        this.count = res.data.count;
        this.dataLoading = false;
      })
      .catch(err => {
        this.$Message.error(err);
        this.dataLoading = false;
      });
  },
  methods: {
    /**
     * 换页的事件处理
     * @param page 页索引
     * @returns {*}
     */
    onPageChanged(page) {
      this.dataLoading = true;
      listUserModels(page)
        .then(res => {
          this.UsersList = res.data.results;
          this.dataLoading = false;
        })
        .catch(err => {
          this.$Message.error(err);
          this.dataLoading = false;
        });
    }
  }
};
</script>

<style scoped>
.model-viewer-description-center {
  display: block;
  width: 800px;
  margin: 0 auto;
  overflow: auto;
}
</style>
