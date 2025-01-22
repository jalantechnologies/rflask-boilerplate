import React, { useState, useEffect, PropsWithChildren } from 'react';
import { Link } from 'react-router-dom';

import routes from '../../constants/routes';
import { useTodoContext } from '../../contexts';
import { Todo } from '../../types';
import { Spinner } from '../index';

import { H2Header } from '../index';

import TodoItem from './todo-item';

interface TodoItemsProps {
  isDashboard?: boolean;
}

const TodoList: React.FC<PropsWithChildren<TodoItemsProps>> = ({
  isDashboard = false,
}) => {
  const { getTodos, getTodosError, isGetTodosLoading } = useTodoContext();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [fetchTodosError, setFetchTodosError] = useState<string>('');
  const limit = isDashboard ? 3 : 0;

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await getTodos(limit);
        if (response) {
          setTodos(response);
        } else {
          setFetchTodosError('Error fetching todos');
        }
      } catch (error) {
        setFetchTodosError('Error fetching todos');
      }
    };

    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    // noinspection JSIgnoredPromiseFromCall
    fetchTodos();
  }, [getTodos, limit]);

  if (fetchTodosError) {
    return <div>Error loading todos: {fetchTodosError}</div>;
  }

  if (getTodosError) {
    return <div>Error loading todos: {getTodosError.message}</div>;
  }

  return (
    <section className="bg-blue-50 px-4 py-10">
      <div className="container m-auto lg:container">
        <H2Header>{isDashboard ? 'Recent Todos' : 'Todo List'}</H2Header>

        <div className="mb-6 flex justify-center gap-4">
          {isDashboard ? (
            <Link
              to={routes.TODOS}
              className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              View All
            </Link>
          ) : (
            <Link
              to={routes.DASHBOARD}
              className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              Dashboard
            </Link>
          )}
          <Link
            to={routes.CREATE_TODO}
            className="rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700"
          >
            Create Todo
          </Link>
        </div>

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
export default TodoList;
