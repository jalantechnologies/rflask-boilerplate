import clsx from 'clsx';
import * as React from 'react';

import HorizontalStackLayout from '../layouts/horizontal-stack-layout';

import styles from './input.styles';
import ErrorBoundary from '../../error/ErrorBoundary';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  endEnhancer?: React.ReactElement | string;
  error: string;
  handleInputRef?: (ref: HTMLInputElement) => void;
  index?: number;
  startEnhancer?: React.ReactElement | string;
  testId?: string;
  textAlign?: 'left' | 'center' | 'right';
  type?: string;
}

const Input: React.FC<InputProps> = ({
  endEnhancer,
  error,
  handleInputRef,
  index,
  startEnhancer,
  testId,
  textAlign = 'left',
  type,
  ...props
}) => (
  <ErrorBoundary>
    <div
      className={clsx([
        styles.inputContainer,
        error ? styles.border.errorState : styles.border.normalState,
      ])}
    >
      <ErrorBoundary>
        <HorizontalStackLayout gap={2}>
          {startEnhancer && (
            <ErrorBoundary>
              <span className="flex h-full min-w-6 items-center justify-center">
                {startEnhancer}
              </span>
            </ErrorBoundary>
          )}
          <ErrorBoundary>
            <input
              {...props}
              autoComplete="off"
              className={clsx([
                styles.input,
                textAlign ? styles.textAlign[textAlign] : '',
              ])}
              data-testid={testId}
              type={type || 'text'}
              ref={handleInputRef ? (ref) => handleInputRef(ref) : null}
            />
          </ErrorBoundary>
          {endEnhancer && (
            <ErrorBoundary>
              <span className="flex h-full min-w-6 items-center justify-center">
                {endEnhancer}
              </span>
            </ErrorBoundary>
          )}
        </HorizontalStackLayout>
      </ErrorBoundary>
    </div>
  </ErrorBoundary>
);

export default Input;
