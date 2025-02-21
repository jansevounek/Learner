import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '@/supabase/init.js'
import { getContainer, getLesson, getUserExtra } from '@/supabase/getFunctions'
import HomePage from '@/views/HomePage.vue'
import ResetPasswordPage from '@/views/auth/ResetPasswordPage.vue'
import UpdateUserPage from '@/views/auth/UpdateUserPage.vue'
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
      meta: { 
        requiresTeam: true,
        requiresDesktop: true
      },
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
      meta: { 
        requiresLessonOwner: true,
        requiresDesktop: true
      },
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
    if (user[0].id == lesson[0].creator_id) {
      next("/");
      return
    }
    // taken from https://stackoverflow.com/questions/7378228/check-if-an-element-is-present-in-an-array
    if (user[0].teams.includes(lesson[0].team_id)) {
      if (to.meta.requiresDesktop) {
        // taken from https://www.geeksforgeeks.org/how-to-detect-whether-the-website-is-being-opened-in-a-mobile-device-or-a-desktop-in-javascript/
        if (isMobile()) {
          next("/");
        } else {
          next();
        }
      } else {
        next();
      }
    } else {
      next("/");
    }
  } else {
    next("/");
  }
}

function isMobile() {
  let details = navigator.userAgent; 

  let regexp = /android|iphone|kindle|ipad/i; 
  let isMobileDevice = regexp.test(details);

  return isMobileDevice
}

async function getLessonOwnership(to, next) {
    const container = await getContainer({ id : to.params.id })
    const user = await getUserExtra()
    
    if (container.length > 0) {
      const lesson = await getLesson({ id : container[0].lesson_id })

      if (lesson.length > 0) {
        if (lesson[0].creator_id == user[0].id) {
          if (to.meta.requiresDesktop) {
            // taken from https://www.geeksforgeeks.org/how-to-detect-whether-the-website-is-being-opened-in-a-mobile-device-or-a-desktop-in-javascript/
            if (isMobile()) {
              next("/");
            } else {
              next();
            }
          } else {
            next();
          }
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
