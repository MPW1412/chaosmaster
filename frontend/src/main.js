import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import vuetify from './plugins/vuetify';
// import axios from 'axios';

Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  render: h => h(App),

  // mounted () {
  //   axios
  //     .get('https://api.coindesk.com/v1/bpi/currentprice.json')
  //     .then(response => (
  //             console.log(response),
  //             this.info = response
  //     ))
  // }  
}).$mount('#app')
