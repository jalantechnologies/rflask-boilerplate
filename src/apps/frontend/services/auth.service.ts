import { AccessToken, ApiResponse, PhoneNumber } from '../types';

import APIService from './api.service';

export default class AuthService extends APIService {
  login = async (
    username: string,
    password: string,
  ): Promise<ApiResponse<AccessToken>> =>
    this.apiClient.post('/access-tokens', {
      username,
      password,
    });

  signup = async (
    firstName: string,
    lastName: string,
    username: string,
    password: string,
  ): Promise<ApiResponse<void>> =>
    this.apiClient.post('/account', {
      first_name: firstName,
      last_name: lastName,
      username: username,
      password: password,
    });

  sendOTP = async (phoneNumber: PhoneNumber): Promise<ApiResponse<void>> =>
    this.apiClient.post('/account', {
      phoneNumber,
    });

  verifyOTP = async (
    phoneNumber: PhoneNumber,
    otp: string,
  ): Promise<ApiResponse<AccessToken>> =>
    this.apiClient.post('/access-tokens', {
      phoneNumber,
      otpCode: otp,
    });
}
