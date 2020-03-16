// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import {Message,Loading} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Axios from 'axios'
import store from './store/index'

Vue.config.productionTip = false

Vue.use(ElementUI);

// 设置axios默认配置
Axios.defaults.baseURL='http://118.31.12.178:8000/api/';
// 添加全局拦截器
Axios.interceptors.request.use(config => {
    config.headers.token=window.sessionStorage.getItem('token');
    console.log('token' + window.sessionStorage.getItem('token'))
    Loading.service({text:"拼命加载中..."});
    return config
});
//  响应拦截
Axios.interceptors.response.use(res=> {
  Loading.service().close();
    // if (res.status == 200) {
    //   return res;
    // }else if(res.status == 201){
    //   Message.error({message: '201错误'});
    //   return Promise.reject(res);
    // }
    return res;
  }, err=> {
    Loading.service().close();
    console.log(err);
    var msg = err.response.data.message;
    if (err.response.status == 500||err.response.status == 404) {
        Message.error({message: '服务器被吃了⊙﹏⊙∥:' + msg});
      } else if (err.response.status == 403) {
        Message.error({message: '权限不足,请联系管理员!' + msg});
      }else if (err.response.status == 401) {
        Message.error({message: '登录认证失败:' + msg});
        router.push({name: 'login'});
      }else if (err.response.status == 429) {
        Message.error({message: '请勿频繁刷新！' + msg});
      } else {
        Message.error({message: '未知错误，请联系管理员' + msg});
      }
      // console.log(Promise.reject(err));
      return Promise.reject(err);
});
// 挂载实例对象
Vue.prototype.$axios = Axios;



// global css
import './assets/css/global.css'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
