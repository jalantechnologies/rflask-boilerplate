import React, { useState, useEffect, PropsWithChildren } from 'react';

import { useTodoContext } from '../../contexts';
import { Todo } from '../../types';
import Spinner from '../spinner/spinner';

import TodoItem from './TodoItem';

interface TodoItemsProps {
  isDashboard?: boolean;
}

const TodoItems: React.FC<PropsWithChildren<TodoItemsProps>> = ({
  isDashboard = false,
}) => {
  const { getTodos, getTodosError, isGetTodosLoading } = useTodoContext();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [fetchTodosError, setFetchTodosError] = useState<string>('');
  const limit = isDashboard ? 3 : 0;

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await getTodos(limit);
        if (response) {
          setTodos(response);
        } else {
          setFetchTodosError('Error fetching tasks');
        }
      } catch (error) {
        setFetchTodosError('Error fetching tasks');
      }
    };

    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    fetchTasks();
  }, [getTodos, limit]);

  if (fetchTodosError) {
    return <div>Error loading tasks: {fetchTodosError}</div>;
  }

  if (getTodosError) {
    return <div>Error loading tasks: {getTodosError.message}</div>;
  }

  return (
    <section className="bg-blue-50 px-4 py-10">
      <div className="container m-auto lg:container">
        <h2 className="mb-6 text-center text-3xl font-bold text-boxdark">
          {isDashboard ? 'Recent Todos' : 'Todo List'}
        </h2>

        {isGetTodosLoading ? (
          <Spinner />
        ) : (
          <div className="grid grid-cols-1 gap-6 px-3 md:grid-cols-3">
            {todos.map((todo: Todo) => (
              <TodoItem key={todo.id} todo={todo} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
};
export default TodoItems;
