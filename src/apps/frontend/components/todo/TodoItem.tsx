import React from 'react';
import { useTodo } from '../../contexts/TodoContext';

type Props = {
  todo: any;
};

const TodoItem: React.FC<Props> = ({ todo }) => {
  const { handleUpdate, handleDelete } = useTodo();

  const isDone = todo.status === 'done';

  return (
    <div className="flex justify-between p-2 border-b items-center">
      <div>
        <p
          className={`font-medium ${isDone ? 'line-through text-gray-500' : ''}`}
        >
          {todo.title}
        </p>
        <p className={`text-sm ${isDone ? 'text-gray-400' : 'text-gray-500'}`}>
          {todo.description}
        </p>
        <p className="text-xs text-gray-400">
          Due: {todo.due_date?.split('T')[0]}
        </p>
        <p className="text-xs italic text-gray-400">Status: {todo.status}</p>
      </div>
      <div className="flex flex-col gap-1 items-end">
        <button
          onClick={() =>
            handleUpdate(todo.id, {
              status: isDone ? 'todo' : 'done',
            })
          }
          className={`text-sm ${isDone ? 'text-yellow-600' : 'text-green-600'}`}
        >
          {isDone ? 'Undo' : 'Complete'}
        </button>
        <button
          onClick={() => handleDelete(todo.id)}
          className="text-sm text-red-500"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TodoItem;
