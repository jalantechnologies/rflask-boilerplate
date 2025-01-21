const routes = {
  ABOUT: '/about',
  DASHBOARD: '/',
  FORGOT_PASSWORD: '/forgot-password',
  LOGIN: '/login',
  RESET_PASSWORD: '/accounts/:accountId/reset_password',
  OTP: '/login?auth_mode=otp',
  PHONE_LOGIN: '/signup?auth_mode=otp',
  SIGNUP: '/signup',
  TODOS: '/todos',
  CREATE_TODO: '/todos/create',
  VIEW_TODO: '/todos/:id',
  EDIT_TODO: '/todos/:id/edit',
  DELETE_TODO: '/todos/:id/delete',
};

export default routes;
