import { AccessToken, ApiResponse, OTPCode, PhoneNumber } from '../types';
import { JsonObject } from '../types/common-types';

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
      username,
      password,
    });

  login = async (
    username: string,
    password: string,
  ): Promise<ApiResponse<AccessToken>> => {
    const response = await this.apiClient.post<JsonObject>('/access-tokens', {
      username,
      password,
    });
    return new ApiResponse(new AccessToken(response.data));
  };

  sendOTP = async (phoneNumber: PhoneNumber): Promise<ApiResponse<OTPCode>> => {
    const response = await this.apiClient.post<JsonObject>('/accounts', {
      phone_number: {
        country_code: phoneNumber.countryCode,
        phone_number: phoneNumber.phoneNumber,
      },
    });
    return new ApiResponse(new OTPCode(response.data));
  }

  verifyOTP = async (
    phoneNumber: PhoneNumber,
    otp: string,
  ): Promise<ApiResponse<AccessToken>> => {
    const response = await this.apiClient.post<JsonObject>('/access-tokens', {
      phone_number: {
        country_code: phoneNumber.countryCode,
        phone_number: phoneNumber.phoneNumber,
      },
      otp_code: otp,
    });
    return new ApiResponse(new AccessToken(response.data));
  };
}
