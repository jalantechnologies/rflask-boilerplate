import React, { createContext, useContext } from 'react';
import { Task } from '../types/task';
import { TaskService } from '../services';
import useAsync from './async.hook';
import { AsyncError, AsyncResult } from '../types';
import { Nullable } from '../types/common-types';

type TaskContextType = {
  getTaskList: () => Promise<Nullable<Task[]>>;
  isTaskListLoading: boolean;
  taskListError: Nullable<AsyncError>;
  taskList: Task[] | null;
};

const taskService = new TaskService();

const TaskContext = createContext<TaskContextType>({
  getTaskList: async () => [],
  isTaskListLoading: false,
  taskListError: null,
  taskList: [] as Task[],
});

export const useTaskContext = (): TaskContextType => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};

const handleGetTaskList = async (): Promise<AsyncResult<Task[]>> => {
  try {
    const apiResponse = await taskService.getTaskListAPI();
    return { data: apiResponse.data ?? [] };
  } catch (error) {
    return { data: [], error };
  }
};

export const TaskProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const {
    isLoading: isTaskListLoading,
    error: taskListError,
    result: taskList = [], // Ensure taskList is never null
    asyncCallback: getTaskList,
  } = useAsync<Task[]>(handleGetTaskList);

  return (
    <TaskContext.Provider
      value={{
        isTaskListLoading,
        taskListError,
        taskList,
        getTaskList,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
};
