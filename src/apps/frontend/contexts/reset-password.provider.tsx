import React, {
  createContext,
  PropsWithChildren,
  ReactNode,
  useContext,
} from 'react';

import { ResetPasswordParams } from '../pages/authentication/reset-password/reset-password-form.hook';
import { ResetPasswordService } from '../services';
import { ApiResponse, AsyncError } from '../types';
import { Nullable } from '../types/common-types';

import useAsync from './async.hook';

type ResetPasswordContextType = {
  isResetPasswordLoading: boolean;
  isSendForgotPasswordEmailLoading: boolean;
  resetPassword: (params: ResetPasswordParams) => Promise<Nullable<void>>;
  resetPasswordError: Nullable<AsyncError>;
  sendForgotPasswordEmail: (username: string) => Promise<Nullable<void>>;
  sendForgotPasswordEmailError: Nullable<AsyncError>;
};

const ResetPasswordContext =
  createContext<Nullable<ResetPasswordContextType>>(null);

const resetPasswordService = new ResetPasswordService();

export const useResetPasswordContext = (): ResetPasswordContextType =>
  useContext(ResetPasswordContext) as ResetPasswordContextType;

const resetPasswordFn = async (
  params: ResetPasswordParams,
): Promise<ApiResponse<void>> => resetPasswordService.resetPassword(params);

const sendForgotPasswordEmailFn = async (
  username: string,
): Promise<ApiResponse<void>> =>
  resetPasswordService.sendForgotPasswordEmail(username);

export const ResetPasswordProvider: React.FC<PropsWithChildren<ReactNode>> = ({
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
