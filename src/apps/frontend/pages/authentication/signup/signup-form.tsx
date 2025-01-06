import React from 'react';
import { Link } from 'react-router-dom';

import {
  Button,
  Flex,
  FormControl,
  Input,
  PasswordInput,
  VerticalStackLayout,
} from '../../../components';
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';
import { ButtonKind, ButtonType } from '../../../types/button';

import useSignupForm from './signup-form.hook';
import ErrorBoundary from '../../../error/ErrorBoundary';

interface SignupFormProps {
  onError: (error: AsyncError) => void;
  onSuccess: () => void;
}

const SignupForm: React.FC<SignupFormProps> = ({ onError, onSuccess }) => {
  const { formik, isSignupLoading } = useSignupForm({ onSuccess, onError });

  return (
    <ErrorBoundary>
      <form onSubmit={formik.handleSubmit}>
        <ErrorBoundary>
          <VerticalStackLayout gap={5}>
            <ErrorBoundary>
              <Flex gap={6}>
                <ErrorBoundary>
                  <div className="w-full">
                    <ErrorBoundary>
                      <FormControl
                        label={'First name'}
                        error={
                          formik.touched.firstName && formik.errors.firstName
                        }
                      >
                        <ErrorBoundary>
                          <Input
                            error={
                              formik.touched.firstName &&
                              formik.errors.firstName
                            }
                            data-testid="firstName"
                            disabled={isSignupLoading}
                            name="firstName"
                            onBlur={formik.handleBlur}
                            onChange={formik.handleChange}
                            placeholder="Enter your first name"
                            value={formik.values.firstName}
                          />
                        </ErrorBoundary>
                      </FormControl>
                    </ErrorBoundary>
                  </div>
                </ErrorBoundary>
                <ErrorBoundary>
                  <div className="w-full">
                    <ErrorBoundary>
                      <FormControl
                        label={'Last name'}
                        error={
                          formik.touched.lastName && formik.errors.lastName
                        }
                      >
                        <ErrorBoundary>
                          <Input
                            error={
                              formik.touched.lastName && formik.errors.lastName
                            }
                            data-testid="lastName"
                            disabled={isSignupLoading}
                            name="lastName"
                            onBlur={formik.handleBlur}
                            onChange={formik.handleChange}
                            placeholder="Enter your last name"
                            value={formik.values.lastName}
                          />
                        </ErrorBoundary>
                      </FormControl>
                    </ErrorBoundary>
                  </div>
                </ErrorBoundary>
              </Flex>
            </ErrorBoundary>
            <ErrorBoundary>
              <FormControl
                label={'Email'}
                error={formik.touched.username && formik.errors.username}
              >
                <ErrorBoundary>
                  <Input
                    data-testid="username"
                    disabled={isSignupLoading}
                    endEnhancer={
                      <ErrorBoundary>
                        <img
                          alt="email icon"
                          className="fill-current opacity-50"
                          src="/assets/img/icon/email.svg"
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
                    name={'password'}
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                    placeholder={'Enter your password'}
                    value={formik.values.password}
                  />
                </ErrorBoundary>
              </FormControl>
            </ErrorBoundary>
            <ErrorBoundary>
              <FormControl
                label={'Re-type Password'}
                error={
                  formik.touched.retypePassword && formik.errors.retypePassword
                }
              >
                <ErrorBoundary>
                  <PasswordInput
                    error={
                      formik.touched.retypePassword &&
                      formik.errors.retypePassword
                    }
                    name={'retypePassword'}
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                    placeholder={'Re-enter the password'}
                    value={formik.values.retypePassword}
                  />
                </ErrorBoundary>
              </FormControl>
            </ErrorBoundary>

            <ErrorBoundary>
              <Button
                type={ButtonType.SUBMIT}
                kind={ButtonKind.PRIMARY}
                isLoading={isSignupLoading}
              >
                Sign Up
              </Button>
            </ErrorBoundary>
            <ErrorBoundary>
              <p className="self-center font-medium">
                Already have an account?{' '}
                <ErrorBoundary>
                  <Link to={routes.LOGIN} className="text-primary">
                    Log in
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

export default SignupForm;
