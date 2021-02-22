import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
// import VueJsonp from 'vue-jsonp'
import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css'
import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import router from './router'
import store from './store'

Vue.config.productionTip = false
Vue.use(ViewUI)
Vue.use(VueAxios, axios)
// Vue.use(VueJsonp)
Vue.use(VueQuillEditor)
axios.defaults.baseURL = 'v1/internal'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
