// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Axios from 'axios'

Vue.config.productionTip = false

Vue.use(ElementUI)
Axios.defaults.baseURL='http://118.31.12.178/api/'
Axios.interceptors.request.use(config => {
    config.headers.token=window.sessionStorage.getItem('token')
    return config
})
Vue.prototype.$axios = Axios



// global css
import './assets/css/global.css'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
