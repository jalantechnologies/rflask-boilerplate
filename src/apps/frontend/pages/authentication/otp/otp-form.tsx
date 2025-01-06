import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ErrorBoundary } from '../../../error/ErrorBoundary';

import {
  Button,
  Flex,
  FormControl,
  OTP,
  VerticalStackLayout,
} from '../../../components';
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';
import { ButtonKind, ButtonType } from '../../../types/button';

import useOTPForm from './otp-form-hook';

interface OTPFormProps {
  isResendEnabled: boolean;
  onError: (error: AsyncError) => void;
  onResendOTPSuccess: () => void;
  onVerifyOTPSuccess: () => void;
  timerRemainingSeconds: string;
}

const OTPForm: React.FC<OTPFormProps> = ({
  isResendEnabled,
  onError,
  onResendOTPSuccess,
  onVerifyOTPSuccess,
  timerRemainingSeconds,
}) => {
  const {
    countryCode,
    formik,
    phoneNumber,
    isVerifyOTPLoading,
    handleResendOTP,
  } = useOTPForm({
    onError,
    onResendOTPSuccess,
    onVerifyOTPSuccess,
  });

  const navigate = useNavigate();

  useEffect(() => {
    if (!phoneNumber || !countryCode) {
      navigate(routes.PHONE_LOGIN);
    }
  }, [phoneNumber, countryCode, navigate]);

  const handleChange = (value: string[]) => {
    formik
      .setFieldValue('otp', value)
      .then()
      .catch((error) => {
        onError(error as AsyncError);
      });
  };

  return (
    <ErrorBoundary>
      <form onSubmit={formik.handleSubmit}>
        <ErrorBoundary>
          <VerticalStackLayout gap={5}>
            <ErrorBoundary>
              <FormControl
                label={`Enter the 4 digit code sent to the mobile number ${countryCode} ${phoneNumber}`}
                error={formik.touched.otp && (formik.errors.otp as string)}
              >
                <ErrorBoundary>
                  <OTP
                    error={formik.touched.otp && (formik.errors.otp as string)}
                    isLoading={isVerifyOTPLoading}
                    onError={onError}
                    onBlur={formik.handleBlur}
                    onChange={handleChange}
                  />
                </ErrorBoundary>
              </FormControl>
            </ErrorBoundary>

            <ErrorBoundary>
              <Flex gap={2}>
                <p className="text-lg text-black">Did not receive a code?</p>
                <ErrorBoundary>
                  <Button
                    disabled={!isResendEnabled}
                    kind={ButtonKind.TERTIARY}
                    onClick={handleResendOTP}
                  >
                    {isResendEnabled
                      ? 'Resend'
                      : `Resend OTP in 00: ${timerRemainingSeconds}`}
                  </Button>
                </ErrorBoundary>
              </Flex>
            </ErrorBoundary>

            <Button
              type={ButtonType.SUBMIT}
              isLoading={isVerifyOTPLoading}
              kind={ButtonKind.PRIMARY}
            >
              Verify
            </Button>
          </VerticalStackLayout>
        </ErrorBoundary>
      </form>
    </ErrorBoundary>
  );
};

export default OTPForm;
