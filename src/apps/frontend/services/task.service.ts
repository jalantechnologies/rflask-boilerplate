import APIService from './api.service';

export interface TaskPayload {
    taskId: string,
    title: string;
    description: string;
    type: 'Official' | 'Personal' | 'Hobby';
    dueDate: string;
}

export interface ApiResponse<T> {
    data: T;
    message: string;
    success: boolean;
}

export default class TaskService extends APIService {
    addTask = async (task: Partial<TaskPayload>,): Promise<ApiResponse<void>> =>
        this.apiClient.post('/tasks', {
            title: task.title,
            description: task.description,
            type: task.type,
            due_date: task.dueDate,
        });

    getTasks = async (): Promise<ApiResponse<TaskPayload[]>> =>
        this.apiClient.get('/tasks');

    deleteTask = async (task: Partial<TaskPayload>): Promise<ApiResponse<void>> =>
        this.apiClient.delete(`/tasks/${task.taskId}`);

    updateTask = async (
        task: Partial<TaskPayload>,
    ): Promise<ApiResponse<void>> =>
        this.apiClient.put(`/tasks/${task.taskId}`, task);
}
