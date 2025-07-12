import Vue from 'vue'
import VueRouter from 'vue-router'

import LoginPage from '@/components/LoginPage.vue'
import HomePage from '@/HomePage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token');
      if (!token) {
        next({ name: 'Login' });
      } else {
        next();
      }
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

// Глобальная проверка авторизации
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router
