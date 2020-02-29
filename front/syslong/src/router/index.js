import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/Login'
import Home from '@/components/Home'
import Welcome from '@/components/Welcome'
import Users from '@/components/user/Users'
import Perms from '@/components/perm/Perms'
import Roles from '@/components/perm/Roles'

Vue.use(Router);

const router =  new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      redirect: '/welcome',
      children: [
        {path: '/welcome', component: Welcome},
        {path: '/users', component: Users},
        {path: '/perms', component: Perms},
        {path: '/roles', component: Roles},
      ]
    }
  ]
});

router.beforeEach((to, from, next) => {
    if (to.path==='/login') return next()
    var token = window.sessionStorage.getItem('token')
    if (!token) return next('/login')
    next()
})

export default router
