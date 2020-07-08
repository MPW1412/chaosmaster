import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home'
import HomeNew from '../components/HelloWorld'
import Images from '../components/Images';

Vue.use(Router)

export default new Router ({

  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/home',
      name: 'homenew',
      component: HomeNew
    },
    {
      path: '/objects/:uuid',
      name: 'Images',
      component: Images,
      props: true

    },
    {
      path: '*',
      redirect: '/'
    }
  ],
  mode:'history'
})

// const router = new VueRouter({
//   mode: 'history',
//   base: process.env.BASE_URL,
//   routes
// })

// export default router
