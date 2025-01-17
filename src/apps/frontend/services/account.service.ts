import { Account, AccessToken, ApiResponse } from '../types';

import APIService from './api.service';

export default class AccountService extends APIService {
  getAccountDetails = async (
    accessToken: AccessToken,
  ): Promise<ApiResponse<Account>> => {
    return this.apiClient.get(`/accounts/${accessToken.accountId}`, {
      headers: {
        Authorization: `Bearer ${accessToken.token}`,
      },
    });
  };
}
