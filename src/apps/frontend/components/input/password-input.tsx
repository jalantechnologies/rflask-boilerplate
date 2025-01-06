import React, { useState } from 'react';

import { ButtonKind } from '../../types/button';
import Button from '../button';
import ErrorBoundary from '../../error/ErrorBoundary';
import Input from '.';

interface PasswordInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  error: string;
  name: string;
  placeholder: string;
  testId?: string;
}

const PasswordInput: React.FC<PasswordInputProps> = ({
  error,
  name,
  placeholder,
  testId,
  ...props
}) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const togglePasswordVisibility = (
    e: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    e.preventDefault();
    setIsPasswordVisible((prevState) => !prevState);
  };

  return (
    <ErrorBoundary>
      <Input
        data-testid="password"
        endEnhancer={
          <ErrorBoundary>
            <Button
              onClick={togglePasswordVisibility}
              kind={ButtonKind.SECONDARY}
            >
              {isPasswordVisible ? (
                <ErrorBoundary>
                  <img
                    className="size-6.5 opacity-65"
                    src="/assets/img/icon/eye-closed.svg"
                    alt="hide password icon"
                  />
                </ErrorBoundary>
              ) : (
                <ErrorBoundary>
                  <img
                    className="size-6.5 opacity-65"
                    src="/assets/img/icon/eye-open.svg"
                    alt="show password icon"
                  />
                </ErrorBoundary>
              )}
            </Button>
          </ErrorBoundary>
        }
        {...props}
        error={error}
        testId={testId}
        name={name}
        placeholder={placeholder}
        type={isPasswordVisible ? 'text' : 'password'}
      />
    </ErrorBoundary>
  );
};

export default PasswordInput;
