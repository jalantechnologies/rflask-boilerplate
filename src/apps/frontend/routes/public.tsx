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

const currentAuthMechanism = Config.getConfigValue<string>(
  'authenticationMechanism',
);

export const publicRoutes = [
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
  publicRoutes.push(
    {
      path: routes.LOGIN,
      element: <PhoneLogin />,
    },
    {
      path: routes.VERIFY_OTP,
      element: <OTPVerificationPage />,
    },
  );
}

if (currentAuthMechanism === constant.EMAIL_BASED_AUTHENTICATION) {
  publicRoutes.push(
    {
      path: routes.LOGIN,
      element: <Login />,
    },
    {
      path: routes.SIGNUP,
      element: <Signup />,
    },
  );
}
