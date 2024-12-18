import React, { createContext, PropsWithChildren, useContext } from 'react';

import TaskService from '../services/task.service'; // Ensure service is correctly imported
import { TaskPayload, ApiResponse, AsyncError } from '../types';
import useAsync from './async.hook';

// Define TaskContext type
type TaskContextType = {
  isAddTaskLoading: boolean;
  isGetTasksLoading: boolean;
  isUpdateTaskLoading: boolean;
  isDeleteTaskLoading: boolean;
  addTask: (task: Partial<TaskPayload>) => Promise<void>;
  addTaskError: AsyncError;
  getTasks: () => Promise<TaskPayload[]>;
  getTasksError: AsyncError;
  deleteTask: (taskId: string) => Promise<void>;
  deleteTaskError: AsyncError;
  updateTask: (task: Partial<TaskPayload>) => Promise<void>;
  updateTaskError: AsyncError;
};

// Create TaskContext
const TaskContext = createContext<TaskContextType | null>(null);

const taskService = new TaskService();

// Hook to access the TaskContext
export const useTaskContext = (): TaskContextType => useContext(TaskContext);

// Task operations
const addTaskFn = async (task: Partial<TaskPayload>): Promise<ApiResponse<void>> =>
  taskService.addTask(task);

const getTasksFn = async (): Promise<ApiResponse<TaskPayload[]>> =>
  taskService.getTasks();

const deleteTaskFn = async (task: Partial<TaskPayload>): Promise<ApiResponse<void>> =>
  taskService.deleteTask(task);

const updateTaskFn = async (
  task: Partial<TaskPayload>,
): Promise<ApiResponse<void>> => taskService.updateTask(task);

// TaskProvider component
export const TaskProvider: React.FC<PropsWithChildren> = ({ children }) => {
  const {
    asyncCallback: addTask,
    error: addTaskError,
    isLoading: isAddTaskLoading,
  } = useAsync(addTaskFn);

  const {
    asyncCallback: getTasks,
    error: getTasksError,
    isLoading: isGetTasksLoading,
  } = useAsync(getTasksFn);

  const {
    asyncCallback: deleteTask,
    error: deleteTaskError,
    isLoading: isDeleteTaskLoading,
  } = useAsync(deleteTaskFn);

  const {
    asyncCallback: updateTask,
    error: updateTaskError,
    isLoading: isUpdateTaskLoading,
  } = useAsync(updateTaskFn);

  return (
    <TaskContext.Provider
      value={{
        isAddTaskLoading,
        isGetTasksLoading,
        isUpdateTaskLoading,
        isDeleteTaskLoading,
        addTask,
        addTaskError,
        getTasks,
        getTasksError,
        deleteTask,
        deleteTaskError,
        updateTask,
        updateTaskError,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
};
