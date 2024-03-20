import React from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

import { H2, VerticalStackLayout } from '../../../components';
import ParagraphMedium from '../../../components/typography/paragraph-medium';
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';
import AuthenticationFormLayout from '../authentication-form-layout';
import AuthenticationPageLayout from '../authentication-page-layout';

import ResetPasswordForm from './reset-password-form';

export const ResetPassword: React.FC = () => {
  const navigate = useNavigate();

  const onSuccess = () => {
    toast.success(
      'Your password has been successfully updated. Please login to continue.',
    );
    navigate(routes.LOGIN);
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };

  return (
    <AuthenticationPageLayout>
      <AuthenticationFormLayout>
        <VerticalStackLayout gap={6}>
          <H2>Reset Password</H2>
          <ParagraphMedium>Setup your new password here</ParagraphMedium>
          <ResetPasswordForm onSuccess={onSuccess} onError={onError} />
        </VerticalStackLayout>
      </AuthenticationFormLayout>
    </AuthenticationPageLayout>
  );
};

export default ResetPassword;
