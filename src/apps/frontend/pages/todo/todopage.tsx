import React from 'react';
import TodoForm from '../../components/todo/todoform';
import TodoList from '../../components/todo/todolist';
import { useTodo } from '../../contexts/todocontext';

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
