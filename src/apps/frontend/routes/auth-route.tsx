import React from 'react';
import { useLocation } from 'react-router-dom';
import ErrorBoundary from '../error/ErrorBoundary';

interface AuthRouteProps {
  authPage: React.FC;
  otpAuthPage: React.FC;
}

const AuthRoute: React.FC<AuthRouteProps> = ({
  authPage: AuthPage,
  otpAuthPage: OTPAuthPage,
}) => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const authMode = queryParams.get('auth_mode');

  return authMode === 'otp' ? (
    <ErrorBoundary>
      <OTPAuthPage />
    </ErrorBoundary>
  ) : (
    <ErrorBoundary>
      <AuthPage />
    </ErrorBoundary>
  );
};

export default AuthRoute;
