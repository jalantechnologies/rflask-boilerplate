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
import { CustomLayout } from '../../../components/layouts/custom-layout.component'; // Import CustomLayout
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';
import { ButtonKind, ButtonType } from '../../../types/button';
import { FieldVisibility } from '../../../types/form';

import useSignupForm from './signup-form.hook';

interface SignupFormProps {
  onError: (error: AsyncError) => void;
  onSuccess: () => void;
  layoutType?: string; // Add layoutType prop
  fieldVisibility?: FieldVisibility;
}

const SignupForm: React.FC<SignupFormProps> = ({
  onError,
  onSuccess,
  layoutType = 'default',
  fieldVisibility = {
    showFirstName: true,
    showLastName: true,
    showEmail: true,
    showPassword: true,
    showRetypePassword: true,
    showSignUpButton: true,
    showLoginLink: true,
  },
}) => {
  const { formik, isSignupLoading } = useSignupForm({ onSuccess, onError });

  return (
    <CustomLayout layoutType={layoutType}>
      {' '}
      <form onSubmit={formik.handleSubmit}>
        <VerticalStackLayout gap={5}>
          {fieldVisibility.showFirstName && fieldVisibility.showLastName && (
            <Flex gap={6}>
              {fieldVisibility.showFirstName && (
                <div className="w-full">
                  <FormControl
                    label={'First name'}
                    error={
                      formik.touched.firstName ? formik.errors.firstName : ''
                    }
                  >
                    <Input
                      error={
                        formik.touched.firstName ? formik.errors.firstName : ''
                      }
                      data-testid="firstName"
                      disabled={isSignupLoading}
                      name="firstName"
                      onBlur={formik.handleBlur}
                      onChange={formik.handleChange}
                      placeholder="Enter your first name"
                      value={formik.values.firstName}
                    />
                  </FormControl>
                </div>
              )}
              {fieldVisibility.showLastName && (
                <div className="w-full">
                  <FormControl
                    label={'Last name'}
                    error={
                      formik.touched.lastName ? formik.errors.lastName : ''
                    }
                  >
                    <Input
                      error={
                        formik.touched.lastName ? formik.errors.lastName : ''
                      }
                      data-testid="lastName"
                      disabled={isSignupLoading}
                      name="lastName"
                      onBlur={formik.handleBlur}
                      onChange={formik.handleChange}
                      placeholder="Enter your last name"
                      value={formik.values.lastName}
                    />
                  </FormControl>
                </div>
              )}
            </Flex>
          )}
          {fieldVisibility.showEmail && (
            <FormControl
              label={'Email'}
              error={formik.touched.username ? formik.errors.username : ''}
            >
              <Input
                data-testid="username"
                disabled={isSignupLoading}
                endEnhancer={
                  <img
                    alt="email icon"
                    className="fill-current opacity-50"
                    src="/assets/img/icon/email.svg"
                  />
                }
                error={formik.touched.username ? formik.errors.username : ''}
                name="username"
                onBlur={formik.handleBlur}
                onChange={formik.handleChange}
                placeholder="Enter your email"
                value={formik.values.username}
              />
            </FormControl>
          )}
          {fieldVisibility.showPassword && (
            <FormControl
              label={'Password'}
              error={formik.touched.password ? formik.errors.password : ''}
            >
              <PasswordInput
                error={formik.touched.password ? formik.errors.password : ''}
                name={'password'}
                onBlur={formik.handleBlur}
                onChange={formik.handleChange}
                placeholder={'Enter your password'}
                value={formik.values.password}
              />
            </FormControl>
          )}
          {fieldVisibility.showRetypePassword && (
            <FormControl
              label={'Re-type Password'}
              error={
                formik.touched.retypePassword
                  ? formik.errors.retypePassword
                  : ''
              }
            >
              <PasswordInput
                error={
                  formik.touched.retypePassword
                    ? formik.errors.retypePassword
                    : ''
                }
                name={'retypePassword'}
                onBlur={formik.handleBlur}
                onChange={formik.handleChange}
                placeholder={'Re-enter the password'}
                value={formik.values.retypePassword}
              />
            </FormControl>
          )}
          {fieldVisibility.showSignUpButton && (
            <Button
              type={ButtonType.SUBMIT}
              kind={ButtonKind.PRIMARY}
              isLoading={isSignupLoading}
            >
              Sign Up
            </Button>
          )}
          {fieldVisibility.showLoginLink && (
            <p className="self-center font-medium">
              Already have an account?{' '}
              <Link to={routes.LOGIN} className="text-primary">
                Log in
              </Link>
            </p>
          )}
        </VerticalStackLayout>
      </form>
    </CustomLayout>
  );
};

export default SignupForm;
