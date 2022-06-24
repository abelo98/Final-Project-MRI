import Vue from "vue";
import router from "./router/router.js";
import App from "./App.vue"
import vSelect from 'vue-select'

Vue.config.productionTip = false;
Vue.component('v-select', vSelect)

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
