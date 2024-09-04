import React from 'react';
import toast from 'react-hot-toast';

import { H2, VerticalStackLayout } from '../../../components';
import { AsyncError } from '../../../types';
import AuthenticationFormLayout from '../authentication-form-layout';
import AuthenticationPageLayout from '../authentication-page-layout';

import PhoneLoginForm from './phone-login-form';

export const PhoneLogin: React.FC = () => {
  const onSendOTPSuccess = () => {
    toast.success('OTP has been sent successfully. Please check your messages.');
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };

  return (
    <AuthenticationPageLayout>
      <AuthenticationFormLayout>
        <VerticalStackLayout gap={8}>
          <H2>Log In</H2>
          <PhoneLoginForm onError={onError} onSendOTPSuccess={onSendOTPSuccess} />
        </VerticalStackLayout>
      </AuthenticationFormLayout>
    </AuthenticationPageLayout>
  );
};

export default PhoneLogin;
