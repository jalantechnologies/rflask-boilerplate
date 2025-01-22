import { Todo, AccessToken, ApiResponse } from '../types';
import { JsonObject } from '../types/common-types';

import APIService from './api.service';

export default class TodoService extends APIService {
  getTodos = async (limit: number): Promise<ApiResponse<Todo[]>> => {
    const userAccessToken = new AccessToken(
      JSON.parse(localStorage.getItem('access-token')) as JsonObject,
    );

    return this.apiClient.get(
      `/todos?account_id=${userAccessToken.accountId}&limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${userAccessToken.token}`,
        },
      },
    );
  };

  getTodo = async (todoId: string): Promise<ApiResponse<Todo>> => {
    const userAccessToken = new AccessToken(
      JSON.parse(localStorage.getItem('access-token')) as JsonObject,
    );

    return this.apiClient.get(`/todos/${todoId}`, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
    });
  };

  createTodo = async (todo: Partial<Todo>): Promise<ApiResponse<Todo>> => {
    const userAccessToken = new AccessToken(
      JSON.parse(localStorage.getItem('access-token')) as JsonObject,
    );

    return this.apiClient.post('/todos', todo, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
    });
  };

  updateTodo = async (todo: Partial<Todo>): Promise<ApiResponse<Todo>> => {
    const userAccessToken = new AccessToken(
      JSON.parse(localStorage.getItem('access-token')) as JsonObject,
    );

    const { id, ...updatedTodo } = todo;

    return this.apiClient.patch(`/todos/${id}`, updatedTodo, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
    });
  };

  deleteTodo = async (todoId: string): Promise<ApiResponse<void>> => {
    const userAccessToken = new AccessToken(
      JSON.parse(localStorage.getItem('access-token')) as JsonObject,
    );

    return this.apiClient.delete(`/todos/${todoId}`, {
      headers: {
        Authorization: `Bearer ${userAccessToken.token}`,
      },
    });
  };
}
