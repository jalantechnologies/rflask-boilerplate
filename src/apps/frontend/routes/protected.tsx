import React, { useEffect } from 'react';
import toast from 'react-hot-toast';
import { Outlet, useNavigate } from 'react-router-dom';

import routes from '../constants/routes';
import { useAccountContext, useAuthContext } from '../contexts';
import { Dashboard, NotFound } from '../pages';
import AppLayout from '../pages/app-layout/app-layout';
import { AsyncError } from '../types';
import ErrorBoundary from '../error/ErrorBoundary';

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
    <ErrorBoundary>
      <AppLayout>
        <ErrorBoundary>
          <Outlet />
        </ErrorBoundary>
      </AppLayout>
    </ErrorBoundary>
  );
};

export const protectedRoutes = [
  {
    path: '',
    element: <App />,
    children: [
      { path: '', element: <Dashboard /> },
      { path: '*', element: <NotFound /> },
    ],
  },
];
