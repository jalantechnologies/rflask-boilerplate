// src/apps/frontend/services/todo.service.ts
import APIService from './api.service';
import { Todo } from '../types/todo';

const api = new APIService(); // uses the configured axios instance with auth header
const API_BASE_URL = '/todos'; // baseURL is already set to /api in APIService

export const fetchTodos = async (): Promise<Todo[]> => {
  const response = await api.apiClient.get(API_BASE_URL);
  return response.data.map((item: any) => new Todo(item));
};

export const updateTodo = async (id: string, data: any) => {
  const response = await api.apiClient.patch(`${API_BASE_URL}/${id}`, data);
  return response.data;
};

export const deleteTodo = async (id: string) => {
  await api.apiClient.delete(`${API_BASE_URL}/${id}`);
};

export const createTodo = async (data: any) => {
  const response = await api.apiClient.post(API_BASE_URL, data);
  return response.data;
};
