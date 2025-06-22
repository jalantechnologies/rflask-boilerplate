// src/apps/frontend/contexts/TodoContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import {
  fetchTodos,
  updateTodo,
  deleteTodo,
  createTodo,
} from '../services/todo.service';

const TodoContext = createContext<any>(null);

export const TodoProvider = ({ children }: { children: React.ReactNode }) => {
  const [todos, setTodos] = useState([]);

  const loadTodos = async () => {
    const data = await fetchTodos();
    setTodos(data);
  };

  const handleUpdate = async (id: string, updatedData: any) => {
    await updateTodo(id, updatedData);
    await loadTodos();
  };

  const handleDelete = async (id: string) => {
    await deleteTodo(id);
    setTodos(todos.filter((todo: any) => todo.id !== id));
  };

  const handleCreate = async (newData: any) => {
    await createTodo(newData);
    await loadTodos();
  };

  useEffect(() => {
    loadTodos();
  }, []);

  return (
    <TodoContext.Provider
      value={{
        todos,
        refresh: loadTodos,
        loadTodos,
        handleUpdate,
        handleDelete,
        handleCreate,
      }}
    >
      {children}
    </TodoContext.Provider>
  );
};

export const useTodo = () => useContext(TodoContext);
