import React from 'react';
import { Navigate } from 'react-router-dom';

import routes from '../constants/routes';
import { ResetPasswordProvider } from '../contexts';
import {
  About, ForgotPassword, ResetPassword, Signup,
} from '../pages';
import Login from '../pages/login';

export const publicRoutes = [
  {
    path: routes.LOGIN,
    element: <Login />,
  },
  {
    path: routes.FORGOT_PASSWORD,
    element: <ResetPasswordProvider><ForgotPassword /></ResetPasswordProvider>,
  },
  {
    path: routes.RESET_PASSWORD,
    element: <ResetPasswordProvider><ResetPassword /></ResetPasswordProvider>,
  },
  {
    path: routes.SIGNUP,
    element: <Signup />,
  },
  { path: routes.ABOUT, element: <About /> },
  { path: '*', element: <Navigate to={routes.LOGIN} /> },
];
