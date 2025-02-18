import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ServiceprosignupView from '@/views/ServiceprosignupView.vue'
import AdminView from '@/views/admin/AdminView.vue'
import CreateServiceView from '@/views/admin/CreateServiceView.vue'
import store from '@/store'

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

    },
    {
      path: '/admin',
      name: "admin-view",
      component: AdminView,
      children: [
        {
          path: 'createservice',
          name: 'admin-create-service',
          component: CreateServiceView
        }
      ] 
    }
  ],
})


router.beforeEach((to) =>{
  if(!store.getters.getRoles.includes('admin') && to.fullPath.startsWith('/admin')){
    router.push('/');
  }

})
export default router
