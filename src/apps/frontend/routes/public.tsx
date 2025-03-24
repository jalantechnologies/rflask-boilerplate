import React from 'react';
import { Navigate } from 'react-router-dom';

import constant from '../constants';
import routes from '../constants/routes';
import { ResetPasswordProvider } from '../contexts';
import { Config } from '../helpers';
import {
  About,
  ForgotPassword,
  Login,
  OTPVerificationPage,
  PhoneLogin,
  ResetPassword,
  Signup,
} from '../pages';

import AuthRoute from './auth-route';

const currentAuthMechanism = Config.getConfigValue<string>(
  'authenticationMechanism',
);

export const publicRoutes = [
  {
    path: routes.LOGIN,
    element: <AuthRoute authPage={Login} otpAuthPage={PhoneLogin} />,
  },
  {
    path: routes.FORGOT_PASSWORD,
    element: (
      <ResetPasswordProvider>
        <ForgotPassword />
      </ResetPasswordProvider>
    ),
  },
  {
    path: routes.RESET_PASSWORD,
    element: (
      <ResetPasswordProvider>
        <ResetPassword />
      </ResetPasswordProvider>
    ),
  },
  { path: routes.ABOUT, element: <About /> },
  { path: '*', element: <Navigate to={routes.LOGIN} /> },
];

if (currentAuthMechanism === constant.PHONE_NUMBER_BASED_AUTHENTICATION) {
  publicRoutes.push({
    path: routes.VERIFY_OTP,
    element: <OTPVerificationPage />,
  });
}

if (currentAuthMechanism === constant.EMAIL_BASED_AUTHENTICATION) {
  publicRoutes.push({
    path: routes.SIGNUP,
    element: <Signup />,
  });
}
