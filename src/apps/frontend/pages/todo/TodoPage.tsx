// pages/todo/TodoPage.tsx
import React from 'react';
import TodoForm from '../../components/todo/TodoForm';
import TodoList from '../../components/todo/TodoList';
import { useTodo } from '../../contexts/TodoContext';

const TodoPage = () => {
  const { refresh } = useTodo();

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">TODO</h1>
      <TodoForm onCreate={refresh} />
      <TodoList />
    </div>
  );
};

export default TodoPage;
