import React, { PropsWithChildren, useState } from 'react';
import { FaTag, FaPencilAlt, FaTrash } from 'react-icons/fa';
import { Link } from 'react-router-dom';

import { Todo } from '../../types';

interface TodoItemProps {
  todo: Todo;
}

const TodoItem: React.FC<PropsWithChildren<TodoItemProps>> = ({ todo }) => {
  const [showFullDescription, setShowFullDescription] = useState(false);

  let { description } = todo;

  if (!showFullDescription) {
    description = `${description.substring(0, 90)}...`;
  }

  return (
    <div className="relative rounded-xl bg-white shadow-md">
      <div className="p-4">
        <div className="mb-6">
          <div className="my-2 text-graydark">
            {todo.completed ? 'Completed' : 'Pending'}
          </div>
          <h3 className="text-xl font-bold">{todo.title}</h3>
        </div>

        <div className="mb-5">{description}</div>

        <button
          onClick={() => setShowFullDescription((prevState) => !prevState)}
          className="mb-5 text-blue-700 hover:text-blue-800"
        >
          {showFullDescription ? 'Read Less' : 'Read More'}
        </button>

        {todo.completed ? (
          <h3 className="mb-2 text-green-500">
            Completed: {todo.completedDate}
          </h3>
        ) : (
          <h3 className="mb-2 text-orange-700">Due: {todo.dueDate}</h3>
        )}

        <div className="mb-5 border border-graydark"></div>

        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center text-orange-700">
            <FaTag className="mr-2 text-lg" />
            {todo.type}
          </div>
          <div className="flex space-x-2">
            <Link
              to={`/todos/${todo.id}/update`}
              className="flex h-[36px] items-center justify-center rounded-lg bg-yellow-400 px-4 py-2 text-center text-sm text-white hover:bg-yellow-500"
            >
              <FaPencilAlt />
            </Link>
            <Link
              to={`/todos/${todo.id}/delete`}
              className="flex h-[36px] items-center justify-center rounded-lg bg-red-600 px-4 py-2 text-center text-sm text-white hover:bg-red-700"
            >
              <FaTrash />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
export default TodoItem;
