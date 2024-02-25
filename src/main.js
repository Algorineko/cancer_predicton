import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'; //引用bootstrap的样式
import 'bootstrap/dist/js/bootstrap.min.js'; //引用bootstrap的js
// 引用bootstrap文件上传
import 'bootstrap-fileinput/css/fileinput.min.css'
import 'bootstrap-fileinput/js/fileinput.min.js'
// import 'bootstrap-fileinput/js/fileinput_locale_zh.js'


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
