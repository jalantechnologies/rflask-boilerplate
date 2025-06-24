import React from 'react';
import { useTodo } from '../../contexts/todocontext';
import { TodoStatus } from '../../types/todo';
import HorizontalStackLayout from '../layouts/horizontal-stack-layout';

type Props = {
  todo: any;
};

const TodoItem: React.FC<Props> = ({ todo }) => {
  const { handleUpdate, handleDelete } = useTodo();
  const isDone = todo.status === TodoStatus.Done;

  return (
    <HorizontalStackLayout className="justify-between items-start p-4 border rounded bg-white shadow-sm">
      <div className="flex-1 pr-4">
        <p
          className={`font-semibold text-lg ${isDone ? 'line-through text-gray-500' : ''}`}
        >
          {todo.title}
        </p>
        <p className={`text-sm ${isDone ? 'text-gray-400' : 'text-gray-600'}`}>
          {todo.description}
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Due:{' '}
          {todo.due_date
            ? new Intl.DateTimeFormat('en-GB', {
                day: '2-digit',
                month: 'short',
                year: 'numeric',
              }).format(new Date(todo.due_date))
            : 'N/A'}
        </p>
        <p className="text-xs italic text-gray-400">Status: {todo.status}</p>
      </div>

      <div className="flex flex-col gap-2">
        {!isDone && (
          <button
            className="btn btn-sm btn-success"
            onClick={() => handleUpdate(todo.id, { status: TodoStatus.Done })}
          >
            Mark Done
          </button>
        )}
        <button
          onClick={() => handleDelete(todo.id)}
          className="btn btn-sm btn-error"
        >
          Delete
        </button>
      </div>
    </HorizontalStackLayout>
  );
};

export default TodoItem;
