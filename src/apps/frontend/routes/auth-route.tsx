import React from 'react';

import constant from '../constants';
import { Config } from '../helpers';

interface AuthRouteProps {
  authPage: React.FC;
  otpAuthPage: React.FC;
}

const AuthRoute: React.FC<AuthRouteProps> = ({
  authPage: AuthPage,
  otpAuthPage: OTPAuthPage,
}) => {
  const currentAuthMechanism = Config.getConfigValue<string>(
    'authenticationMechanism',
  );

  return currentAuthMechanism === constant.PHONE_NUMBER_BASED_AUTHENTICATION ? (
    <OTPAuthPage />
  ) : (
    <AuthPage />
  );
};

export default AuthRoute;
