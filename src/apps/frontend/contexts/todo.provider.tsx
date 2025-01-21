import React, { createContext, PropsWithChildren, useContext } from 'react';

import { TodoService } from '../services';
import { Todo, ApiResponse, AsyncError } from '../types';

import useAsync from './async.hook';

type TodoContextType = {
  // Get Todos
  getTodos: (limit: number) => Promise<Todo[]>;
  getTodosError: AsyncError;
  isGetTodosLoading: boolean;

  // Create Todo
  // eslint-disable-next-line @typescript-eslint/member-ordering
  createTodo: (todo: Partial<Todo>) => Promise<Todo>;
  createTodoError: AsyncError;
  isCreateTodoLoading: boolean;

  // Update Todo
  updateTodo: (todo: Partial<Todo>) => Promise<Todo>;
  updateTodoError: AsyncError;
  // eslint-disable-next-line @typescript-eslint/member-ordering
  isUpdateTodoLoading: boolean;

  // Delete Todo
  // eslint-disable-next-line @typescript-eslint/member-ordering
  deleteTodo: (todoId: string) => Promise<void>;
  deleteTodoError: AsyncError;
  isDeleteTodoLoading: boolean;
};

const TodoContext = createContext<TodoContextType | null>(null);

const todoService = new TodoService();

export const useTodoContext = (): TodoContextType => useContext(TodoContext);

const getTodosFn = async (limit: number): Promise<ApiResponse<Todo[]>> =>
  todoService.getTodos(limit);

const createTodoFn = async (todo: Partial<Todo>): Promise<ApiResponse<Todo>> =>
  todoService.createTodo(todo);

const updateTodoFn = async (todo: Partial<Todo>): Promise<ApiResponse<Todo>> =>
  todoService.updateTodo(todo);

const deleteTodoFn = async (todoId: string): Promise<ApiResponse<void>> =>
  todoService.deleteTodo(todoId);

export const TodoProvider: React.FC<PropsWithChildren> = ({ children }) => {
  const {
    isLoading: isGetTodosLoading,
    error: getTodosError,
    asyncCallback: getTodos,
  } = useAsync(getTodosFn);

  const {
    isLoading: isCreateTodoLoading,
    error: createTodoError,
    asyncCallback: createTodo,
  } = useAsync(createTodoFn);

  const {
    isLoading: isUpdateTodoLoading,
    error: updateTodoError,
    asyncCallback: updateTodo,
  } = useAsync(updateTodoFn);

  const {
    isLoading: isDeleteTodoLoading,
    error: deleteTodoError,
    asyncCallback: deleteTodo,
  } = useAsync(deleteTodoFn);

  return (
    <TodoContext.Provider
      value={{
        // Get Todos
        getTodos,
        getTodosError,
        isGetTodosLoading,

        // Create Todo
        createTodo,
        createTodoError,
        isCreateTodoLoading,

        // Update Todo
        updateTodo,
        updateTodoError,
        isUpdateTodoLoading,

        // Delete Todo
        deleteTodo,
        deleteTodoError,
        isDeleteTodoLoading,
      }}
    >
      {children}
    </TodoContext.Provider>
  );
};
