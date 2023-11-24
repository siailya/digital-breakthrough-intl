import {createRouter, createWebHashHistory} from 'vue-router'
import SingleClassificationView from '@/views/SingleView.vue'
import PackageView from "@/views/PackageView.vue";
import ParsingView from "@/views/ParsingView.vue";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      redirect: '/classification',
    },
    {
      path: '/classification',
      name: 'classification',
      component: SingleClassificationView,
    },
    {
      path: '/package',
      name: 'package',
      component: PackageView,
    },
    {
      path: '/parsing',
      name: 'parsing',
      component: ParsingView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      redirect: '/classification',
    },
  ]
})

export default router
