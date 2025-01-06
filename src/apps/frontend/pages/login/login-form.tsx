import React from 'react';
import { Link } from 'react-router-dom';

import {
  VerticalStackLayout,
  FormControl,
  PasswordInput,
  Flex,
  Button,
  Input,
} from '../../components';
import routes from '../../constants/routes';
import { AsyncError } from '../../types';
import { ButtonType, ButtonKind } from '../../types/button';

import LoginFormCheckbox from './login-form-checkbox';
import useLoginForm from './login-form.hook';
import ErrorBoundary from '../../error/ErrorBoundary';

interface LoginFormProps {
  onSuccess: () => void;
  onError: (error: AsyncError) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onError, onSuccess }) => {
  const { formik, isLoginLoading } = useLoginForm({ onSuccess, onError });

  return (
    <ErrorBoundary>
      <form onSubmit={formik.handleSubmit}>
        <ErrorBoundary>
          <VerticalStackLayout gap={5}>
            <ErrorBoundary>
              <FormControl
                label={'Email'}
                error={formik.touched.username && formik.errors.username}
              >
                <ErrorBoundary>
                  <Input
                    data-testid="username"
                    disabled={isLoginLoading}
                    endEnhancer={
                      <ErrorBoundary>
                        <img
                          className="fill-current opacity-50"
                          src="/assets/img/icon/email.svg"
                          alt="email icon"
                        />
                      </ErrorBoundary>
                    }
                    error={formik.touched.username && formik.errors.username}
                    name="username"
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                    placeholder="Enter your email"
                    value={formik.values.username}
                  />
                </ErrorBoundary>
              </FormControl>
            </ErrorBoundary>
            <ErrorBoundary>
              <FormControl
                label={'Password'}
                error={formik.touched.password && formik.errors.password}
              >
                <ErrorBoundary>
                  <PasswordInput
                    error={formik.touched.password && formik.errors.password}
                    name="password"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    placeholder="Enter your password"
                    value={formik.values.password}
                  />
                </ErrorBoundary>
              </FormControl>
            </ErrorBoundary>

            <ErrorBoundary>
              <Flex alignItems="center" justifyContent="between">
                <ErrorBoundary>
                  <label htmlFor="formCheckbox" className="flex cursor-pointer">
                    <ErrorBoundary>
                      <LoginFormCheckbox />
                    </ErrorBoundary>
                    <ErrorBoundary>
                      <p>Remember me</p>
                    </ErrorBoundary>
                  </label>
                </ErrorBoundary>

                <ErrorBoundary>
                  <Link
                    to={routes.FORGOT_PASSWORD}
                    className="text-sm text-primary hover:underline"
                  >
                    Forget password?
                  </Link>
                </ErrorBoundary>
              </Flex>
            </ErrorBoundary>

            <ErrorBoundary>
              <Flex justifyContent="end">
                <ErrorBoundary>
                  <Link
                    to={routes.PHONE_LOGIN}
                    className="text-sm text-primary hover:underline"
                  >
                    Login with phone number
                  </Link>
                </ErrorBoundary>
              </Flex>
            </ErrorBoundary>

            <ErrorBoundary>
              <Button
                type={ButtonType.SUBMIT}
                kind={ButtonKind.PRIMARY}
                isLoading={isLoginLoading}
              >
                Log In
              </Button>
            </ErrorBoundary>
            <ErrorBoundary>
              <p className="self-center font-medium">
                Don’t have any account?{' '}
                <ErrorBoundary>
                  <Link to={routes.SIGNUP} className="text-primary">
                    Sign Up
                  </Link>
                </ErrorBoundary>
              </p>
            </ErrorBoundary>
          </VerticalStackLayout>
        </ErrorBoundary>
      </form>
    </ErrorBoundary>
  );
};

export default LoginForm;
