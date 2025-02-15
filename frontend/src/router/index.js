import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ServiceprosignupView from '@/views/ServiceprosignupView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login-view',
      component: LoginView,
    },
    { 
      path: '/signup',
      name: 'signup-view',
      component: SignupView,

    },
    { 
      path: '/servicepro-signup',
      name: 'servicepro-signup-view',
      component: ServiceprosignupView,

    }
  ],
})

export default router
