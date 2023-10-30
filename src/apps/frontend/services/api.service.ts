import { AxiosInstance } from 'axios';

import AppService from './app.service';

export default class APIService extends AppService {
  apiClient: AxiosInstance;
  apiUrl: string;

  constructor() {
    super();
    this.apiUrl = `${this.appHost}/api`;
    this.apiClient = APIService.getAxiosInstance({
      baseURL: this.apiUrl,
    });
  }
}
