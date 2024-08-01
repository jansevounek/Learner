import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../supabase/init.js'
import HomePage from '../views/HomePage.vue'
import LoginPage from '../views/auth/LoginPage.vue'
import SignupPage from '../views/auth/SignupPage.vue'
import LearningHomePage from '../views/LearningHomePage.vue'
import ResetPasswordPage from '../views/auth/ResetPasswordPage.vue'
import UpdateUserPage from '../views/auth/UpdateUserPage.vue'
import LectionsPage from '../views/LectionsPage.vue'
import LectionPage from '../views/LectionPage.vue'
import PracticeContainerPage from '../views/PracticeContainerPage.vue'
import FullScreenContainerPage from '../views/FullScreenContainerPage.vue'

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
      path: '/learning/homepage',
      name: 'learninghome',
      component: LearningHomePage,
      meta: { requiresAuth: true },
    },
    {
      path: '/learning/lections',
      name: 'lections',
      component: LectionsPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/learning/container/:port',
      component: PracticeContainerPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/container/:port',
      component: FullScreenContainerPage,
      meta: { requiresAuth: true },
    },
    {
      // taken from https://router.vuejs.org/guide/essentials/dynamic-matching.html
      path: '/learning/lection/:id',
      component: LectionPage,
      meta: { requiresAuth: true },
    }
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
