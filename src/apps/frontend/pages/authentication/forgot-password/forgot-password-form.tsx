import React from 'react';

import {
  Button,
  FormControl,
  Input,
  VerticalStackLayout,
} from '../../../components';
import ParagraphMedium from '../../../components/typography/paragraph-medium';
import { AsyncError } from '../../../types';
import { ButtonType } from '../../../types/button';

import useForgotPasswordForm from './forgot-password-form.hook';
import { ErrorBoundary } from '../../../error/ErrorBoundary';

interface ForgotPasswordFormProps {
  onError: (error: AsyncError) => void;
  onSuccess: (username: string) => void;
}

const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({
  onError,
  onSuccess,
}) => {
  const { formik, isSendForgotPasswordEmailLoading } = useForgotPasswordForm({
    onError,
    onSuccess,
  });

  return (
    <ErrorBoundary>
      <VerticalStackLayout gap={5}>
        <ErrorBoundary>
          <ParagraphMedium>
            Enter your details to receive a reset link
          </ParagraphMedium>
        </ErrorBoundary>
        <ErrorBoundary>
          <form onSubmit={formik.handleSubmit}>
            <ErrorBoundary>
              <VerticalStackLayout gap={5}>
                <ErrorBoundary>
                  <FormControl
                    error={formik.touched.username && formik.errors.username}
                    label={'Email'}
                  >
                    <ErrorBoundary>
                      <Input
                        data-testid="username"
                        disabled={isSendForgotPasswordEmailLoading}
                        error={
                          formik.touched.username && formik.errors.username
                        }
                        endEnhancer={
                          <img
                            alt="email icon"
                            className="fill-current opacity-50"
                            src="assets/img/icon/email.svg"
                          />
                        }
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        name="username"
                        value={formik.values.username}
                        placeholder="Enter your email"
                      />
                    </ErrorBoundary>
                  </FormControl>
                </ErrorBoundary>

                <ErrorBoundary>
                  <Button
                    isLoading={isSendForgotPasswordEmailLoading}
                    type={ButtonType.SUBMIT}
                  >
                    Receive Reset Link
                  </Button>
                </ErrorBoundary>
              </VerticalStackLayout>
            </ErrorBoundary>
          </form>
        </ErrorBoundary>
      </VerticalStackLayout>
    </ErrorBoundary>
  );
};

export default ForgotPasswordForm;
