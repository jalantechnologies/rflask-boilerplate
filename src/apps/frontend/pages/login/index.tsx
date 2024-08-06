import React from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

import { VerticalStackLayout, H2 } from '../../components';
import routes from '../../constants/routes';
import { AsyncError } from '../../types';
import AuthenticationFormLayout from '../authentication/authentication-form-layout';
import AuthenticationPageLayout from '../authentication/authentication-page-layout';

import LoginForm from './login-form';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const onSuccess = () => {
    navigate(routes.DASHBOARD);
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };

  return (
    <AuthenticationPageLayout>
      <AuthenticationFormLayout>
       <VerticalStackLayout gap={8}>
        <H2>Log In</H2>
        <LoginForm onSuccess={onSuccess} onError={onError} />
       </VerticalStackLayout>
      </AuthenticationFormLayout>
    </AuthenticationPageLayout>
  );
};

export default Login;
