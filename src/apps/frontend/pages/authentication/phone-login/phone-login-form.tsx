import React from 'react';
import { Link } from 'react-router-dom';

import {
  Button,
  Flex,
  FormControl,
  Input,
  Select,
  VerticalStackLayout,
} from '../../../components';
import COUNTRY_SELECT_OPTIONS from '../../../constants/countries';
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';
import { ButtonKind, ButtonType } from '../../../types/button';

import usePhoneLoginForm from './phone-login-form.hook';
import { ErrorBoundary } from '../../../error/ErrorBoundary';

interface PhoneLoginFormProps {
  onSendOTPSuccess: () => void;
  onError: (error: AsyncError) => void;
}

const PhoneLoginForm: React.FC<PhoneLoginFormProps> = ({
  onError,
  onSendOTPSuccess,
}) => {
  const { formik, isSendOTPLoading } = usePhoneLoginForm({
    onSendOTPSuccess,
    onError,
  });

  const setFormikFieldValue = (fieldName: string, data: string) => {
    formik
      .setFieldValue(fieldName, data)
      .then()
      .catch((err) => {
        onError(err as AsyncError);
      });
  };

  const handleChangePhone = ({
    target,
  }: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = target;
    setFormikFieldValue('phoneNumber', value);
  };

  const handleChangeSelect = ({
    target,
  }: React.ChangeEvent<HTMLSelectElement>) => {
    const { value } = target;
    const [countryCode, country] = value.split(', ');
    setFormikFieldValue('country', country);
    setFormikFieldValue('countryCode', countryCode);
    setFormikFieldValue('phoneNumber', '');
  };

  return (
    <ErrorBoundary>
      <form onSubmit={formik.handleSubmit}>
        <ErrorBoundary>
          <VerticalStackLayout gap={5}>
            <ErrorBoundary>
              <Flex gap={4}>
                <ErrorBoundary>
                  <FormControl
                    label={'Phone'}
                    error={
                      formik.touched.countryCode && formik.errors.countryCode
                    }
                  >
                    <ErrorBoundary>
                      <Select
                        handleChange={handleChangeSelect}
                        isLoading={isSendOTPLoading}
                        options={COUNTRY_SELECT_OPTIONS}
                        value={`${formik.values.countryCode}, ${formik.values.country}`}
                      />
                    </ErrorBoundary>
                  </FormControl>
                </ErrorBoundary>
                <ErrorBoundary>
                  <div className="w-full">
                    <ErrorBoundary>
                      <FormControl
                        label={''}
                        error={
                          formik.touched.phoneNumber &&
                          formik.errors.phoneNumber
                        }
                      >
                        <ErrorBoundary>
                          <Input
                            data-testid="phoneNumber"
                            disabled={isSendOTPLoading}
                            error={
                              formik.touched.phoneNumber &&
                              formik.errors.phoneNumber
                            }
                            name="phoneNumber"
                            onChange={handleChangePhone}
                            onBlur={formik.handleBlur}
                            placeholder="Enter your phone number"
                            type="number"
                            value={formik.values.phoneNumber}
                          />
                        </ErrorBoundary>
                      </FormControl>
                    </ErrorBoundary>
                  </div>
                </ErrorBoundary>
              </Flex>
            </ErrorBoundary>

            <ErrorBoundary>
              <Flex justifyContent="end">
                <ErrorBoundary>
                  <Link
                    to={routes.LOGIN}
                    className="text-sm text-primary hover:underline"
                  >
                    Login with email
                  </Link>
                </ErrorBoundary>
              </Flex>
            </ErrorBoundary>

            <ErrorBoundary>
              <Button
                type={ButtonType.SUBMIT}
                isLoading={isSendOTPLoading}
                kind={ButtonKind.PRIMARY}
              >
                Get OTP
              </Button>
            </ErrorBoundary>
          </VerticalStackLayout>
        </ErrorBoundary>
      </form>
    </ErrorBoundary>
  );
};

export default PhoneLoginForm;
