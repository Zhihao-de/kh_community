<template>
  <div>
    <div class="upload-images-list" v-for="(file, index) in urls" :key="index">
      <template v-if="file.status === 'finished'">
        <img :src="file.response.url" />
        <div class="upload-images-list-cover">
          <Icon
            type="ios-eye-outline"
            size="25"
            @click.native="viewFile(file)"
          ></Icon>
          <Icon
            type="ios-trash-outline"
            size="25"
            @click.native="confirmDeleteFile(file)"
          ></Icon>
        </div>
      </template>
      <template v-else>
        <Progress
          v-if="file.showProgress"
          :percent="file.percentage"
          hide-info
        ></Progress>
      </template>
    </div>
    <Upload
      ref="upload"
      :show-upload-list="false"
      :default-file-list="initurls"
      :format="['jpg', 'jpeg', 'png', 'bmp']"
      :max-size="512"
      :on-success="onFileUploaded"
      :on-format-error="onFileFormatError"
      :on-exceeded-size="onFileExceedMaxSizeError"
      :before-upload="onBeforeUploadingFile"
      action="/v1/internal/attachments/"
      type="drag"
      style="display: inline-block; width: 100px;"
    >
      <div style="width: 100px;height:100px;line-height: 100px;">
        <Icon type="ios-cloud-upload-outline" size="25"></Icon>
      </div>
    </Upload>
    <Modal title="查看图片" v-model="showImageViewer" :footer-hide="true">
      <img :src="imageURL" v-if="showImageViewer" style="width: 100%" />
    </Modal>
  </div>
</template>

<script>
import { deleteFile } from '@/api/attachment_api'
export default {
  name: 'ImageUpload',
  props: {
    value: Array,
    limit: {
      type: Number,
      default: 1
    }
  },
  watch: {
    value: {
      immediate: true, // 这句重要
      handler (newVal) {
        console.log(newVal)
        this.initurls = !newVal
          ? []
          : newVal.map(item => {
            const kv = item.split(',')
            return {
              name: kv[1].substring(kv[1].lastIndexOf('/') + 1),
              response: {
                id: parseInt(kv[0]),
                url: kv[1]
              },
              status: 'finished'
            }
          })
        this.urls = this.initurls
      }
    }
  },
  data () {
    return {
      initurls: [],
      urls: [],
      imageURL: '',
      showImageViewer: false
    }
  },
  mounted () {
    this.urls = this.$refs.upload.fileList
  },
  methods: {
    getIdUrlPairs (fileList) {
      return fileList.map(file => file.response.id + ',' + file.response.url)
    },
    /**
     * 文件上传前的事件处理
     * @returns {*}
     */
    onBeforeUploadingFile () {
      const check = this.urls.length < this.limit
      if (!check) {
        this.$Notice.warning({
          title: '上传文件的数量超过限制',
          desc:
            '上传文件数量的上限为' +
            this.limit +
            '，请删除不再需要的文件后重试。'
        })
      }
      return check
    },
    /**
     * 文件大小越界错误的事件处理
     * @param file Upload组件使用的文件对象
     * @returns {*}
     */
    onFileExceedMaxSizeError (file) {
      this.$Notice.warning({
        title: '文件大小超限',
        desc:
          '选择的文件 <strong>' +
          file.name +
          '</strong> 超过了 1024KB 的限制，请缩小图片大小后重试。'
      })
    },
    /**
     * 文件格式错误的事件处理
     * @param file Upload组件使用的文件对象
     * @returns {*}
     */
    onFileFormatError (file) {
      this.$Notice.warning({
        title: '文件格式不正确',
        desc:
          '选择的文件 <strong>' +
          file.name +
          '</strong> 的格式不正确，请选择JPG、JPEG、PNG格式的图片后重试。'
      })
    },
    onFileUploaded (resp, file, fileList) {
      console.log('fileuploaded')
      this.$Message.info('操作成功！')
      this.$emit('input', this.getIdUrlPairs(fileList))
    },
    /**
     * 查看已上传的产品图片
     * @param file 图片文件
     * @returns {*}
     */
    viewFile (file) {
      this.imageURL = file.response.url
      this.showImageViewer = true
    },
    confirmDeleteFile (file) {
      this.$Modal.confirm({
        title: '操作确认',
        content: '确定删除图片？',
        onOk: () => {
          this.deleteFile(file)
        },
        onCancel: () => {}
      })
    },
    /**
     * 删除已上传的产品图片
     * @param file Upload组件使用的文件对象
     * @returns {*}
     */
    deleteFile (file) {
      if (file.status !== 'finished') return
      deleteFile(file)
        .then(() => {
          const upload = this.$refs.upload
          upload.fileList.splice(upload.fileList.indexOf(file), 1)
          this.$Message.info('操作成功！')
          //
          this.$emit('input', this.getIdUrlPairs(upload.fileList))
        })
        .catch(err => {
          this.$Message.error(err)
        })
    }
  }
}
</script>

<style>
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
</style>
