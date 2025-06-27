import React from 'react';
import { TodoProvider } from '../../contexts/todocontext';
import TodoForm from '../../components/todo/todoform';
import TodoList from '../../components/todo/todolist';
import { useTodo } from '../../contexts/todocontext';

const TodoContent: React.FC = () => {
  const { refresh } = useTodo();

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-xl font-bold mb-4">Your TODOs</h1>
      <TodoForm onCreate={refresh} />
      <TodoList />
    </div>
  );
};

const TodoPage: React.FC = () => (
  <TodoProvider>
    <TodoContent />
  </TodoProvider>
);

export default TodoPage;
