const routes = {
  ABOUT: '/about',
  DASHBOARD: '/',
  FORGOT_PASSWORD: '/forgot-password',
  LOGIN: '/login',
  OTP: '/login?auth_mode=otp',
  PHONE_LOGIN: '/signup?auth_mode=otp',
  RESET_PASSWORD: '/account/:accountId/reset_password',
  SIGNUP: '/signup',
  TASKS: '/tasks',
};

export default routes;
