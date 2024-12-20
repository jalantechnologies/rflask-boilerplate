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

        getTasks = async (): Promise<ApiResponse<TaskPayload[]>> => {
            const mockTasks: TaskPayload[] = [
                {
                    taskId: '1',
                    title: 'Complete React Project',
                    description: 'Finalize the frontend for the application.',
                    type: 'Official',
                    dueDate: new Date().toISOString().split('T')[0],
                },
                {
                    taskId: '2',
                    title: 'Morning Run',
                    description: 'Run 5km in the park.',
                    type: 'Personal',
                    dueDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString().split('T')[0], // Tomorrow
                },
                {
                    taskId: '3',
                    title: 'Guitar Practice',
                    description: 'Practice chords and scales for 30 minutes.',
                    type: 'Hobby',
                    dueDate: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString().split('T')[0], // Day after tomorrow
                },
                {
                    taskId: '1',
                    title: 'Complete React Project',
                    description: 'Finalize the frontend for the application.',
                    type: 'Official',
                    dueDate: new Date().toISOString().split('T')[0],
                },
                {
                    taskId: '2',
                    title: 'Morning Run',
                    description: 'Run 5km in the park.',
                    type: 'Personal',
                    dueDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString().split('T')[0], // Tomorrow
                },
                {
                    taskId: '3',
                    title: 'Guitar Practice',
                    description: 'Practice chords and scales for 30 minutes.',
                    type: 'Hobby',
                    dueDate: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString().split('T')[0], // Day after tomorrow
                },
            ];
        
            return Promise.resolve({
                data: mockTasks,
                message: 'Mock tasks retrieved successfully.',
                success: true,
            });
        };
        

    deleteTask = async (task: Partial<TaskPayload>): Promise<ApiResponse<void>> =>
        this.apiClient.delete(`/tasks/${task.taskId}`);

    editTask = async (
        task: Partial<TaskPayload>,
    ): Promise<ApiResponse<void>> =>
        this.apiClient.put(`/tasks/${task.taskId}`, task);
}
