import React, { useEffect } from 'react';
import toast from 'react-hot-toast';
import { Outlet, useNavigate } from 'react-router-dom';

import routes from '../constants/routes';
import { useAccountContext, useAuthContext } from '../contexts';
import { Dashboard, NotFound, } from '../pages';
import AppLayout from '../pages/app-layout/app-layout';
import { AsyncError } from '../types';
import AddTask from '../pages/task/add-task';
import TaskList from '../pages/task/get-task';
import EditTask from '../pages/task/edit-task';

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
      { path: 'add-task', element: <AddTask /> },
      { path: 'tasks', element: <TaskList /> },
      { path: 'edit-task/:taskId', element: <EditTask /> },
      { path: '*', element: <NotFound /> },
    ],
  },
];
