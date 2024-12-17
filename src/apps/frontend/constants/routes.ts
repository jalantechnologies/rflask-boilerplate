const routes = {
  ABOUT: '/about',
  DASHBOARD: '/',
  FORGOT_PASSWORD: '/forgot-password',
  LOGIN: '/login',
  RESET_PASSWORD: '/accounts/:accountId/reset_password',
  OTP: '/login?auth_mode=otp',
  PHONE_LOGIN: '/signup?auth_mode=otp',
  SIGNUP: '/signup',
  TASKS: '/tasks',
  ADDTASK:'/add-task'
};

export default routes;
