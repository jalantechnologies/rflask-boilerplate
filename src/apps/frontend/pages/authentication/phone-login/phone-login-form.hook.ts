import { useFormik } from 'formik';
import { PhoneNumberUtil } from 'google-libphonenumber';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';

import constant from '../../../constants';
import routes from '../../../constants/routes';
import { useAuthContext } from '../../../contexts';
import { AsyncError, PhoneNumber } from '../../../types';

interface PhoneLoginFormProps {
  onError: (err: AsyncError) => void;
  onSendOTPSuccess: () => void;
}

const usePhoneLoginForm = ({
  onSendOTPSuccess,
  onError,
}: PhoneLoginFormProps) => {
  const { isSendOTPLoading, sendOTPError, sendOTP } = useAuthContext();

  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      countryCode: '+1',
      country: 'US',
      phoneNumber: '',
    },

    validationSchema: Yup.object({
      phoneNumber: Yup.string().required(constant.PHONE_VALIDATION_ERROR),
    }),

    onSubmit: (values) => {
      const parsedPhoneNumber = PhoneNumberUtil.getInstance().parse(
        values.phoneNumber,
        values.country,
      );
      const isValidPhoneNumber =
        PhoneNumberUtil.getInstance().isValidNumber(parsedPhoneNumber);
      const formattedPhoneNumber = parsedPhoneNumber.getNationalNumber();

      if (!isValidPhoneNumber || !formattedPhoneNumber) {
        onError({ message: constant.PHONE_VALIDATION_ERROR } as AsyncError);
        return;
      }

      const encodedCountryCode = encodeURIComponent(values.countryCode);
      const otpPageUrl = `${routes.LOGIN}?&country_code=${encodedCountryCode}&phone_number=${formattedPhoneNumber}`;

      sendOTP(
        new PhoneNumber({
          country_code: values.countryCode,
          phone_number: formattedPhoneNumber.toString(),
        }),
      )
        .then(() => {
          onSendOTPSuccess();
          navigate(otpPageUrl);
        })
        .catch((err) => {
          onError(err as AsyncError);
        });
    },
  });

  return {
    formik,
    isSendOTPLoading,
    sendOTPError,
  };
};

export default usePhoneLoginForm;
