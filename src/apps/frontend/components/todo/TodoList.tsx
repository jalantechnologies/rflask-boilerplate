import React from 'react';
import { useTodo } from '../../contexts/TodoContext';
import TodoItem from './TodoItem';
import type { Todo } from '../../types/todo';

const TodoList: React.FC = () => {
  const { todos } = useTodo();

  if (todos.length === 0) {
    return <p className="text-gray-500">No TODOs yet.</p>;
  }

  return (
    <div className="space-y-2">
      {todos.map((todo: Todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  );
};

export default TodoList;
