import React, { useRef, useState, FocusEventHandler } from 'react';

import constant from '../../constants';
import { AsyncError, KeyboardKeys } from '../../types';
import FlexItem from '../flex/flex-item.component';
import Flex from '../flex/flex.component';

import OTPInput from './otp-input';

interface OTPProps {
  error: string;
  isLoading: boolean;
  onBlur?: FocusEventHandler<HTMLInputElement>;
  onChange: (values: string[]) => void;
  onError: (error: AsyncError) => void;
}

const OTP: React.FC<OTPProps> = ({ error, isLoading, onBlur, onChange }) => {
  const [otp, setOtp] = useState<string[]>(Array(constant.OTP_LENGTH).fill(''));

  const inputRef = useRef<HTMLInputElement[]>([]);

  const handleInputRef = (ref: HTMLInputElement) => {
    inputRef.current.push(ref);
  };

  const handleOTPChange = (inputValue: string, index: number): void => {
    const otpInputs = [...otp];

    if (inputValue.length >= constant.OTP_INPUT_MAX_LENGTH) return;

    otpInputs[index] = inputValue;
    setOtp(otpInputs);

    if (inputValue.length === 1 && index < constant.OTP_LENGTH - 1) {
      inputRef.current[index + 1]?.focus();
    }

    if (inputValue.length === 0 && index > 0) {
      inputRef.current[index - 1]?.focus();
    }

    onChange(otpInputs);
  };

  const handleOnKeyDown = (
    { key }: React.KeyboardEvent<HTMLInputElement>,
    index: number,
  ) => {
    if (key === KeyboardKeys.BACKSPACE.toString()) {
      inputRef.current[index - 1]?.focus();
    }
  };

  return (
    <Flex gap={6}>
      {otp.map((_, index) => (
        <FlexItem flex="flex1" key={index}>
          <OTPInput
            disabled={isLoading}
            index={index}
            name={'otp'}
            error={error}
            onChange={(e) => handleOTPChange(e.target.value, index)}
            onBlur={onBlur}
            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) =>
              handleOnKeyDown(e, index + 1)
            }
            handleInputRef={handleInputRef}
            value={otp[index]}
          />
        </FlexItem>
      ))}
    </Flex>
  );
};

export default OTP;
