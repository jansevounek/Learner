import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '@/supabase/init.js'
import { getContainer, getLesson, getUserExtra } from '@/supabase/getFunctions'
import HomePage from '@/views/HomePage.vue'
import LoginPage from '@/views/auth/LoginPage.vue'
import SignupPage from '@/views/auth/SignupPage.vue'
import ResetPasswordPage from '@/views/auth/ResetPasswordPage.vue'
import UpdateUserPage from '@/views/auth/UpdateUserPage.vue'
import PracticeContainerPage from '@/views/container/PracticeContainerPage.vue'
import FullScreenContainerPage from '@/views/container/FullScreenContainerPage.vue'
import PaymentPage from '@/views/payments/PaymentPage.vue'
import PaymentCanceledPage from '@/views/payments/PaymentCanceledPage.vue'
import PaymentSuccessfullPage from '@/views/payments/PaymentSuccessfullPage.vue'
import LearningUserPage from '@/views/learning/LearningUserPage.vue'
import LearningAdminPage from '@/views/learning/LearningAdminPage.vue'
import LearningCreateLessonPage from '@/views/learning/LearningCreateLessonPage.vue'
import LessonPage from '@/views/learning/LessonPage.vue'
import LessonSolutionsPage from '@/views/learning/LessonSolutionsPage.vue'
import LearningCheckContainerPage from '@/views/learning/LearningCheckContainerPage.vue'

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
      path: '/learning/admin',
      name: 'admin-lessons',
      component: LearningAdminPage,
      meta: { 
        requiresPremium: true
       },
    },
    {
      path: '/learning/user',
      name: 'user-lessons',
      component: LearningUserPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/learning/create-lesson',
      name: 'create-lesson',
      component: LearningCreateLessonPage,
      meta: { requiresPremium: true },
    },
    {
      path: '/learning/lesson/:id',
      name: 'lesson-do',
      component: LessonPage,
      meta: { requiresTeam: true },
    },
    {
      path: '/learning/solutions/:id',
      name: 'lesson-solutions',
      component: LessonSolutionsPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/learning/solutions/container/:id',
      name: 'lesson-solutions-container',
      component: LearningCheckContainerPage,
      meta: { requiresLessonOwner: true },
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

async function getUserPremium(next) {
  const { data: { user } } = await supabase.auth.getUser()
  if (user) {
    const { data, error } = await supabase
          .from('user')
          .select('premium')
          .eq('user_id', user.id);
    if (error) {
      next("/");
    }
    if (data[0].premium) {
      next();
    } else {
      next("/");
    }
  } else {
    next("/")
  }
}

async function getUserTeam(to, next) {
  const user = await getUserExtra()
  const lesson = await getLesson({ id : to.params.id })

  if (user && lesson) {
    // taken from https://stackoverflow.com/questions/7378228/check-if-an-element-is-present-in-an-array
    if (user[0].teams.includes(lesson[0].team_id)) {
      next();
    } else {
      next("/");
    }
  } else {
    next("/");
  }
}

async function getLessonOwnership(to, next) {
    const container = await getContainer({ id : to.params.id })
    const user = await getUserExtra()
    
    if (container.length > 0) {
      const lesson = await getLesson({ id : container[0].lesson_id })

      if (lesson.length > 0) {
        if (lesson[0].creator_id == user[0].id) {
          next();
        } else {
          next("/")
        }
      } else {
        next("/")
      }
    } else {
      next("/")
    }
}

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    await getUserAuth(next);
  } else if (to.meta.requiresPremium) {
    await getUserPremium(next);
  } else if (to.meta.requiresTeam) {
    await getUserTeam(to, next)
  } else if (to.meta.requiresUnAuth) {
    await getUserUnAuth(next);
  } else if (to.meta.requiresLessonOwner) {
    await getLessonOwnership(to, next)
  } else {
    next();
  }
});

export default router
