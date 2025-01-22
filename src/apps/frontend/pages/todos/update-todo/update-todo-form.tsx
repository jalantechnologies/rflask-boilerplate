import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { TodoForm } from '../../../components';
import { useTodoContext } from '../../../contexts';
import { AsyncError, Todo } from '../../../types';

interface CreateTodoFormProps {
  onError: (error: AsyncError) => void;
  onSuccess: () => void;
}

const UpdateTodoForm: React.FC<CreateTodoFormProps> = ({
  onError,
  onSuccess,
}) => {
  const todoId = useParams().id;

  const { getTodo, getTodoError } = useTodoContext();
  const [todo, setTodo] = useState<Todo>();
  const [fetchTodoError, setFetchTodoError] = useState<string>('');

  useEffect(() => {
    const fetchTodo = async () => {
      try {
        const response = await getTodo(todoId);
        if (response) {
          setTodo(response);
        } else {
          setFetchTodoError('Error fetching todos');
        }
      } catch (error) {
        setFetchTodoError('Error fetching todos');
      }
    };

    // noinspection JSIgnoredPromiseFromCall
    fetchTodo(); // eslint-disable-line @typescript-eslint/no-floating-promises
  }, [getTodo, todoId]);

  if (fetchTodoError) {
    return <div>Error loading todos: {fetchTodoError}</div>;
  }

  if (getTodoError) {
    return <div>Error loading todos: {getTodoError.message}</div>;
  }

  return <TodoForm todo={todo} onSuccess={onSuccess} onError={onError} />;
};

export default UpdateTodoForm;
