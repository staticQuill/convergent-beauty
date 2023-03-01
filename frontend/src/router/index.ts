import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import RecommendationView from '../views/RecommendationView.vue'
import AddProductView from '../views/AddProductView.vue'
import ProductNotesView from '../views/ProductNotesView.vue'
import { userAuthStore } from "@/stores/auth.store";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/recommendations',
      name: 'recommendations',
      component: RecommendationView
    },
    {
      path: '/new-product',
      name: 'new-product',
      component: AddProductView
    },
    {
      path: '/product-notes',
      name: 'product-notes',
      component: ProductNotesView
    }
  ]
})

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const auth = userAuthStore();

  if (authRequired && !auth.user) {
    auth.returnUrl = to.fullPath;
    return '/login';
  }
});


export default router
