import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ServiceprosignupView from '@/views/ServiceprosignupView.vue'
import AdminView from '@/views/admin/AdminView.vue'
import CreateServiceView from '@/views/admin/CreateServiceView.vue'
import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import ViewServiceView from '@/views/admin/ViewServiceView.vue'
import ServiceProfessionalsView from '@/views/admin/ServiceProfessionalsView.vue'
import CustomerView from '@/views/admin/CustomerView.vue'
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
          path: '',
          name: 'admin-dashboard',
          component: AdminDashboardView,
        },
        {
          path: 'service/view',
          name: 'admin-view-service',
          component: ViewServiceView,
        },
        {
          path: 'service',
          name: 'admin-create-service',
          component: CreateServiceView,
        },
        {
          path: 'service/:id',
          name: 'admin-update-service',
          props: true,
          component: CreateServiceView,
        },
        {
          path: 'service_professionals',
          name: 'admin-view-service_professionals',
          props: true,
          component: ServiceProfessionalsView,
        },
        {
          path: 'customers',
          name: 'admin-view-customers',
          props: true,
          component: CustomerView,
      }
      ] 
    }
  ],
})


router.beforeEach((to) =>{
  if(!store.getters.getRoles.includes('admin') && to.fullPath.startsWith('/admin')){
    router.push('/');
  }
  if(to.fullPath.startsWith("/signout")){
    store.commit("setUser",{token: null, role:[]});
    router.push('/');
  }
})
export default router
