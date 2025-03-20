import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import {
  VerticalStackLayout,
  FormControl,
  PasswordInput,
  Flex,
  Button,
  Input,
} from '../../components';
import { CustomLayout } from '../../components/layouts/custom-layout.component';
import { LayoutType } from '../../components/layouts/layout-config';
import constant from '../../constants';
import routes from '../../constants/routes';
import { Config } from '../../helpers';
import { AsyncError } from '../../types';
import { ButtonType, ButtonKind } from '../../types/button';

import LoginFormCheckbox from './login-form-checkbox';
import useLoginForm from './login-form.hook';

type LoginFields = 'username' | 'password';

interface LoginFormProps {
  onSuccess: () => void;
  onError: (error: AsyncError) => void;
  layoutType?: LayoutType;
}

const LoginForm: React.FC<LoginFormProps> = ({
  onError,
  onSuccess,
  layoutType = LayoutType.Default,
}) => {
  const { formik, isLoginLoading } = useLoginForm({ onSuccess, onError });
  const currentLoginMethod = Config.getConfigValue<string>(
    'authenticationMechanism',
  );

  const navigate = useNavigate();
  useEffect(() => {
    if (currentLoginMethod === constant.PHONE_NUMBER_BASED_AUTHENTICATION) {
      navigate(routes.SIGNUP);
    }
  }, [currentLoginMethod, navigate]);

  const getFormikError = (field: LoginFields) =>
    formik.touched[field] ? formik.errors[field] : '';

  return (
    <CustomLayout layoutType={layoutType}>
      <form onSubmit={formik.handleSubmit}>
        <VerticalStackLayout gap={5}>
          <FormControl label="Email" error={getFormikError('username')}>
            <Input
              data-testid="username"
              disabled={isLoginLoading}
              endEnhancer={
                <img
                  className="fill-current opacity-50"
                  src="/assets/img/icon/email.svg"
                  alt="email icon"
                />
              }
              error={getFormikError('username')}
              name="username"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              placeholder="Enter your email"
              value={formik.values.username}
            />
          </FormControl>
          <FormControl label="Password" error={getFormikError('password')}>
            <PasswordInput
              error={getFormikError('password')}
              name="password"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              placeholder="Enter your password"
              value={formik.values.password}
            />
          </FormControl>
          <Flex alignItems="center" justifyContent="between">
            <label htmlFor="formCheckbox" className="flex cursor-pointer">
              <LoginFormCheckbox />
              <p>Remember me</p>
            </label>

            <Link
              to={routes.FORGOT_PASSWORD}
              className="text-sm text-primary hover:underline"
            >
              Forgot password?
            </Link>
          </Flex>
          <Button
            type={ButtonType.SUBMIT}
            kind={ButtonKind.PRIMARY}
            isLoading={isLoginLoading}
          >
            Log In
          </Button>
          <p className="self-center font-medium">
            Don’t have an account?{' '}
            <Link to={routes.SIGNUP} className="text-primary">
              Sign Up
            </Link>
          </p>
        </VerticalStackLayout>
      </form>
    </CustomLayout>
  );
};

export default LoginForm;
