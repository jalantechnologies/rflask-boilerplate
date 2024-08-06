import { Account, AccessToken, ApiResponse } from '../types';
import { JsonObject } from '../types/common-types';

import APIService from './api.service';

export default class AccountService extends APIService {
  getAccountDetails = async (): Promise<ApiResponse<Account>> => {
    const userAccessToken = new AccessToken(
      JSON.parse(localStorage.getItem('access-token')) as JsonObject,
    );

    return this.apiClient.get(`/accounts/${userAccessToken.accountId}`, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
    });
  };
}
