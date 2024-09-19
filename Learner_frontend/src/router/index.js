import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../supabase/init.js'
import HomePage from '../views/HomePage.vue'
import LoginPage from '../views/auth/LoginPage.vue'
import SignupPage from '../views/auth/SignupPage.vue'
import LearningHomePage from '../views/LearningHomePage.vue'
import ResetPasswordPage from '../views/auth/ResetPasswordPage.vue'
import UpdateUserPage from '../views/auth/UpdateUserPage.vue'
import PracticeContainerPage from '../views/PracticeContainerPage.vue'
import FullScreenContainerPage from '../views/FullScreenContainerPage.vue'
import PaymentPage from '../views/payments/PaymentPage.vue'
import PaymentCanceledPage from '../views/payments/PaymentCanceledPage.vue'
import PaymentSuccessfullPage from '../views/payments/PaymentSuccessfullPage.vue'

let localUser;

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { requiresUnAuth: true }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupPage,
      meta: { requiresUnAuth: true }
    },
    {
      path: '/resetpassword',
      name: 'resetpassword',
      component: ResetPasswordPage,
    },
    {
      path: '/updateuser',
      name: 'updateuser',
      component: UpdateUserPage,
    },
    {
      path: '/payment/getpremium',
      name: 'getpremium',
      component: PaymentPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/payment/failiure',
      name: 'payment-failiure',
      component: PaymentCanceledPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/payment/success',
      name: 'payment-success',
      component: PaymentSuccessfullPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/learning/homepage',
      name: 'learninghome',
      component: LearningHomePage,
      meta: { requiresAuth: true },
    },
    {
      path: '/learning/container/:port',
      name: 'practicecontainer',
      component: PracticeContainerPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/container/:port',
      name: 'fullscreencontainer',
      component: FullScreenContainerPage,
      meta: { requiresAuth: true },
    },
  ]
})

async function getUserAuth(next) {
  localUser = await supabase.auth.getSession();
  if (localUser.data.session == null) {
    next("/login");
  } else {
    next();
  }
}

async function getUserUnAuth(next) {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    next();
  } else {
    next("/");
  }
}

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    await getUserAuth(next);
  } else if (to.meta.requiresUnAuth) {
    await getUserUnAuth(next);
  } else {
    next();
  }
});

export default router
