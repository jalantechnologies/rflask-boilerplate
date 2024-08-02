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

interface LoginFormProps {
  onSuccess: () => void;
  onError: (error: AsyncError) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onError, onSuccess }) => {
  const { formik, isLoginLoading } = useLoginForm({ onSuccess, onError });

  return (
    <form onSubmit={formik.handleSubmit}>
      <VerticalStackLayout gap={5}>
        <FormControl
          label={'Email'}
          error={formik.touched.username && formik.errors.username}
        >
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
            error={formik.touched.username && formik.errors.username}
            name="username"
            onBlur={formik.handleBlur}
            onChange={formik.handleChange}
            placeholder="Enter your email"
            value={formik.values.username}
          />
        </FormControl>
        <FormControl
          label={'Password'}
          error={formik.touched.password && formik.errors.password}
        >
          <PasswordInput
            error={formik.touched.password && formik.errors.password}
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
            Forget password?
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
          Don’t have any account?{' '}
          <Link to={routes.SIGNUP} className="text-primary">
            Sign Up
          </Link>
        </p>
      </VerticalStackLayout>
    </form>
  );
};

export default LoginForm;
