import APIService from './api.service';

export interface TaskPayload {
    title: string;
    description: string;
    type: 'Official' | 'Personal' | 'Hobby';
    dueDate: string; // ISO 8601 format
}

export interface ApiResponse<T> {
    data: T;
    message: string;
    success: boolean;
}

export default class TaskService extends APIService {
    addTask = async (task: TaskPayload): Promise<ApiResponse<void>> =>
        this.apiClient.post('/tasks', {
            title: task.title,
            description: task.description,
            type: task.type,
            due_date: task.dueDate,
        });

    getTasks = async (): Promise<ApiResponse<TaskPayload[]>> =>
        this.apiClient.get('/tasks');

    deleteTask = async (taskId: string): Promise<ApiResponse<void>> =>
        this.apiClient.delete(`/tasks/${taskId}`);

    updateTask = async (
        taskId: string,
        task: Partial<TaskPayload>,
    ): Promise<ApiResponse<void>> =>
        this.apiClient.put(`/tasks/${taskId}`, task);
}
