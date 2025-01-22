import React, { useEffect } from 'react';
import toast from 'react-hot-toast';
import { Outlet, useNavigate } from 'react-router-dom';

import routes from '../constants/routes';
import { useAccountContext, useAuthContext } from '../contexts';
import {
  Dashboard,
  Todos,
  CreateTodo,
  UpdateTodo,
  DeleteTodo,
  NotFound,
} from '../pages';
import AppLayout from '../pages/app-layout/app-layout';
import { AsyncError } from '../types';

const App = () => {
  const { getAccountDetails } = useAccountContext();
  const { logout } = useAuthContext();
  const navigate = useNavigate();

  useEffect(() => {
    getAccountDetails().catch((err: AsyncError) => {
      toast.error(err.message);
      logout();
      navigate(routes.LOGIN);
    });
  }, [getAccountDetails, logout, navigate]);

  return (
    <AppLayout>
      <Outlet />
    </AppLayout>
  );
};

export const protectedRoutes = [
  {
    path: '',
    element: <App />,
    children: [
      { path: '', element: <Dashboard /> },
      { path: 'todos', element: <Todos /> },
      { path: 'todos/create', element: <CreateTodo /> },
      { path: 'todos/:id/update', element: <UpdateTodo /> },
      { path: 'todos/:id/delete', element: <DeleteTodo /> },
      { path: '*', element: <NotFound /> },
    ],
  },
];
