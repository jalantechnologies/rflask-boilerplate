import { AccessToken, ApiError, ApiResponse } from '../types';

import APIService from './api.service';

export default class AuthService extends APIService {
  signup = async (
    firstName: string,
    lastName: string,
    username: string,
    password: string,
  ): Promise<ApiResponse<void>> =>
    this.apiClient.post('/accounts', {
      first_name: firstName,
      last_name: lastName,
      username: username,
      password: password,
    });

  login = async (
    username: string,
    password: string,
  ): Promise<ApiResponse<AccessToken>> => {
    try {
      const response = await this.apiClient.post('/access-tokens', {
        username: username,
        password: password,
      });

      return new ApiResponse(new AccessToken(response.data), undefined);
    } catch (error) {
      return new ApiResponse(undefined, new ApiError(error.response.data));
    }
  };
}
