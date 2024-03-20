import { useFormik } from 'formik';
import * as Yup from 'yup';

import constant from '../../../constants';
import { useAuthContext } from '../../../contexts';
import { AsyncError } from '../../../types';

interface OTPFormProps {
  onError: (error: AsyncError) => void;
  onResendOTPSuccess: () => void;
  onVerifyOTPSuccess: () => void;
}

const useOTPForm = ({
  onError,
  onResendOTPSuccess,
  onVerifyOTPSuccess,
}: OTPFormProps) => {
  const {
    isVerifyOTPLoading,
    sendOTP,
    verifyOTP,
    verifyOTPError,
    verifyOTPResult,
  } = useAuthContext();

  const searchParams = new URLSearchParams(window.location.search);
  const phoneNumber = searchParams.get('phone_number');
  const countryCode = decodeURIComponent(searchParams.get('country_code'));

  const formik = useFormik({
    initialValues: {
      otp: Array(constant.OTP_LENGTH).fill(''),
    },

    validationSchema: Yup.object({
      otp: Yup.array()
        .of(Yup.string().required('')),
    }),

    onSubmit: (values) => {
      const otp = values.otp.join('');

      verifyOTP(
        { countryCode, phoneNumber },
        otp,
      ).then(() => {
        onVerifyOTPSuccess();
      })
        .catch((error) => {
          onError(error as AsyncError);
        });
    },
  });

  const handleResendOTP = () => {
    sendOTP({
      countryCode,
      phoneNumber,
    })
      .then(() => {
        onResendOTPSuccess();
      })
      .catch((error) => {
        onError(error as AsyncError);
      });
  };

  return {
    countryCode,
    formik,
    handleResendOTP,
    isVerifyOTPLoading,
    phoneNumber,
    sendOTP,
    verifyOTPError,
    verifyOTPResult,
  };
};

export default useOTPForm;
