import APIService from './api.service';

export default class AccessService extends APIService {
  login(username: string, password: string): Promise<void> {
    return this.apiClient.post('/access-tokens', {
      username,
      password,
    });
  }
}
