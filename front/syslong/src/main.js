// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import {Message,Loading} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Axios from 'axios'

Vue.config.productionTip = false

Vue.use(ElementUI);

// 设置axios默认配置
Axios.defaults.baseURL='http://118.31.12.178/api/';
// 添加全局拦截器
Axios.interceptors.request.use(config => {
    config.headers.token=window.sessionStorage.getItem('token');
    Loading.service({text:"拼命加载中..."});
    return config
});
//  响应拦截
Axios.interceptors.response.use(res=> {
  Loading.service().close();
    if (res.status == 200) {
      return res;
    }else if(res.status == 201){
      Message.error({message: '201错误'});
      return Promise.reject(res);
    }
    return Promise.reject(res);
  }, err=> {
    Loading.service().close();
    // console.log(err);
    if (err.response.status == 500||err.response.status == 404) {
        Message.error({message: '服务器被吃了⊙﹏⊙∥'});
      } else if (err.response.status == 403) {
        Message.error({message: '权限不足,请联系管理员!'});
      }else if (err.response.status == 401) {
        Message.error({message: '登录认证失败或登录超时！请检查后重试'});
        router.push({name: 'login'});
      }else if (err.response.status == 406) {
        Message.error({message: '已经限速了，请慢行！'});
      } else {
        Message.error({message: '服务器发生未知错误，请联系管理员'});
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
  components: { App },
  template: '<App/>'
})
