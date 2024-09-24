import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Home from '../components/Home.vue'
import Profile from '../components/Profile.vue'

const router = createRouter({
    history: createWebHistory(),
    //base: "/app",
    routes: [
      {
        path: '/',
        component: Home
      },
      {
          path: '/profile',
          name: 'profile',
          component: Profile
      },
    ]  
  })
  
  export default router