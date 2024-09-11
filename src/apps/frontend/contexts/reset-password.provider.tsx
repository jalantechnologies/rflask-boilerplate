import React, { createContext, PropsWithChildren, useContext } from 'react';

import { ResetPasswordParams } from '../pages/authentication/reset-password/reset-password-form.hook';
import { ResetPasswordService } from '../services';
import { ApiResponse, AsyncError } from '../types';

import useAsync from './async.hook';

type ResetPasswordContextType = {
  isResetPasswordLoading: boolean;
  isSendForgotPasswordEmailLoading: boolean;
  resetPassword: (params: ResetPasswordParams) => Promise<void>;
  resetPasswordError: AsyncError;
  sendForgotPasswordEmail: (username: string) => Promise<void>;
  sendForgotPasswordEmailError: AsyncError;
};

const ResetPasswordContext = createContext<ResetPasswordContextType | null>(
  null,
);

const resetPasswordService = new ResetPasswordService();

export const useResetPasswordContext = (): ResetPasswordContextType =>
  useContext(ResetPasswordContext);

const resetPasswordFn = async (
  params: ResetPasswordParams,
): Promise<ApiResponse<void>> => resetPasswordService.resetPassword(params);

const sendForgotPasswordEmailFn = async (
  username: string,
): Promise<ApiResponse<void>> =>
  resetPasswordService.sendForgotPasswordEmail(username);

export const ResetPasswordProvider: React.FC<PropsWithChildren> = ({
  children,
}) => {
  const {
    isLoading: isSendForgotPasswordEmailLoading,
    error: sendForgotPasswordEmailError,
    asyncCallback: sendForgotPasswordEmail,
  } = useAsync(sendForgotPasswordEmailFn);

  const {
    isLoading: isResetPasswordLoading,
    error: resetPasswordError,
    asyncCallback: resetPassword,
  } = useAsync(resetPasswordFn);

  return (
    <ResetPasswordContext.Provider
      value={{
        isResetPasswordLoading,
        isSendForgotPasswordEmailLoading,
        resetPassword,
        resetPasswordError,
        sendForgotPasswordEmail,
        sendForgotPasswordEmailError,
      }}
    >
      {children}
    </ResetPasswordContext.Provider>
  );
};
