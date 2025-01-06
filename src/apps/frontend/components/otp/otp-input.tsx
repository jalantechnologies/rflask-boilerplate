import React, { FocusEventHandler } from 'react';

import Input from '../input';
import ErrorBoundary from '../../error/ErrorBoundary';

type OTPInputProps = {
  disabled: boolean;
  error: string;
  handleInputRef: (ref: HTMLInputElement) => void;
  index: number;
  name: string;
  onBlur?: FocusEventHandler<HTMLInputElement>;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onKeyDown: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  value: string;
};

const OTPInput: React.FC<OTPInputProps> = ({
  disabled,
  error,
  handleInputRef,
  index,
  name,
  onBlur,
  onChange,
  onKeyDown,
  value,
}) => (
  <ErrorBoundary>
    <Input
      disabled={disabled}
      error={error}
      handleInputRef={handleInputRef}
      index={index}
      name={name}
      onBlur={onBlur}
      onChange={onChange}
      onKeyDown={onKeyDown}
      textAlign="center"
      type={'number'}
      value={value}
    />
  </ErrorBoundary>
);

export default OTPInput;
