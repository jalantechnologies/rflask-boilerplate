import React, { useState } from 'react';
import { createTodo } from '../../services/todo.service';
import { TodoType } from '../../types/todo';

type Props = {
  onCreate: () => void;
};

const TodoForm: React.FC<Props> = ({ onCreate }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [type, setType] = useState<TodoType>(TodoType.Personal);
  const [dueDate, setDueDate] = useState('');

  const handleSubmit = async () => {
    await createTodo({
      title,
      description,
      type,
      due_date: dueDate ? `${dueDate}T00:00:00` : null,
    });

    setTitle('');
    setDescription('');
    setType(TodoType.Personal);
    setDueDate('');
    onCreate();
  };

  return (
    <div className="mb-4 bg-gray-50 p-4 rounded shadow">
      <h2 className="text-lg font-semibold mb-2">Create TODO</h2>
      <input
        className="input"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input
        className="input"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <select
        className="input"
        value={type}
        onChange={(e) => setType(e.target.value as TodoType)}
      >
        {Object.values(TodoType).map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <input
        className="input"
        type="date"
        value={dueDate}
        onChange={(e) => setDueDate(e.target.value)}
      />
      <button className="btn btn-primary mt-2" onClick={handleSubmit}>
        Add TODO
      </button>
    </div>
  );
};

export default TodoForm;
