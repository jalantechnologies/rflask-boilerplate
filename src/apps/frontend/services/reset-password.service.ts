import { ResetPasswordParams } from '../pages/authentication/reset-password/reset-password-form.hook';
import { ApiResponse } from '../types';

import APIService from './api.service';

export default class ResetPasswordService extends APIService {
  sendForgotPasswordEmail = async (
    username: string,
  ): Promise<ApiResponse<void>> =>
    this.apiClient.post('/password-reset-tokens', {
      username,
    });

  resetPassword = async (
    params: ResetPasswordParams,
  ): Promise<ApiResponse<void>> => {
    const { accountId, newPassword, token } = params;
    return this.apiClient.patch(`/accounts/${accountId}`, {
      newPassword,
      token,
    });
  };
}
