import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import HomeView from '../views/HomeView.vue'
import RecommendationView from '../views/RecommendationView.vue'
import AddProductView from '../views/AddProductView.vue'
import ProductNotesView from '../views/ProductNotesView.vue'
import UserProductsView from '../views/UserProductsView.vue'
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
      path: '/signup',
      name: 'signup',
      component: SignUpView
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
    },
    {
      path: '/your-products',
      name: 'user-products',
      component: UserProductsView
    }
  ]
})

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/signup'];
  const authRequired = !publicPages.includes(to.path);
  const auth = userAuthStore();
  const user_authenticated = async () => {
    if (!auth.user.refreshToken) {
      return false
    }
    console.log("using refresh token")
    console.log(auth.user.refreshToken)
    const authRequestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({refresh: auth.user.refreshToken}),
    };
    console.log(authRequestOptions)
    const tokenJson = await fetch("http://188.166.174.54/auth/login/refresh/", authRequestOptions);
    const tokens = await tokenJson.json()
    auth.user.bearerToken = "Bearer".concat(" ", tokens.access)
    localStorage.setItem('user', JSON.stringify(auth.user))
    return tokenJson.status === 200;
  }
  if (authRequired && !await user_authenticated()) {
    auth.returnUrl = to.fullPath;
    return '/login';
  }
});


export default router
