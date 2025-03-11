import { ApiError, ApiResponse } from '../types';
import { JsonObject } from '../types/common-types';
import { Task } from '../types/task';
import { getAccessTokenFromStorage } from '../utils/storage-util';

import APIService from './api.service';

export default class TaskService extends APIService {
  getTaskListAPI = async (): Promise<ApiResponse<Task[]>> => {
    try {
      const userAccessToken = getAccessTokenFromStorage();
      const response = await this.apiClient.get('/tasks', {
        headers: {
          Authorization: `Bearer ${userAccessToken?.token}`,
        },
      });
      const tasks: Task[] = Task.fromApiArray(response.data as any[]);

      return new ApiResponse(tasks, undefined);
    } catch (error) {
      return new ApiResponse(
        [],
        new ApiError(error.response.data as JsonObject),
      );
    }
  };
}
