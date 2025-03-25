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
import SearchServiceView from '@/views/user/SearchServiceView.vue'
import UserView from '@/views/user/UserView.vue'
import BookServiceView from '@/views/user/BookServiceView.vue'
import UserDashboardView from '@/views/user/UserDashboardView.vue'
import ServiceProfessionalDashboardView from '@/views/serviceprofessional/ServiceProfessionalDashboardView.vue'
import ServiceProfessionalView from '@/views/serviceprofessional/ServiceProfessionalView.vue'
import RateServiceView from '@/views/user/RateServiceView.vue'
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
          component: ServiceProfessionalsView,
        },
        {
          path: 'customers',
          name: 'admin-view-customers',
          component: CustomerView,
      }
      ] 
    },
    {
      path: '/user',
      name: "user-view",
      component: UserView,
      children: [
        {
          path: '',
          name: 'user-dashboard',
          component: UserDashboardView,
        },
        {
          path: 'search',
          name: 'user-search-service',
          component: SearchServiceView,
        },
        {
          path: 'book/:id',
          name: 'user-book-service',
          props: true,
          component: BookServiceView,
        },
        {
          path: 'feedback/:id',
          name: 'user-feedback-service',
          props: true,
          component: RateServiceView,
        },
      ]
    },
    {
      path: '/service_professional',
      name: "service_professional-view",
      component: ServiceProfessionalView,
      children:[
        {
          path: '',
          name: 'service_professional-dashboard',
          component: ServiceProfessionalDashboardView,
        },
      ]
    }
  ],
})


router.beforeEach((to) =>{
  if(!store.getters.getRoles.includes('admin') && to.fullPath.startsWith('/admin')){
    router.push('/');
  }
  if(!store.getters.getRoles.includes('user') && to.fullPath.startsWith('/user')){
    router.push('/');
  }
  if(!store.getters.getRoles.includes('service_professional') && to.fullPath.startsWith('/service_professional')){
    router.push('/');
  }
  if(to.fullPath.startsWith("/signout")){
    store.commit("setUser",{token: null, role:[]});
    router.push('/');
  }
})
export default router
