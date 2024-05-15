import React, { useEffect } from 'react';
import { Outlet } from 'react-router-dom';

import { useAccountContext } from '../contexts';
import { Dashboard, NotFound, Tasks } from '../pages';
import AppLayout from '../pages/app-layout/app-layout';
import routes from '../constants/routes';

const App = () => {
  const { getAccountDetails } = useAccountContext();

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    getAccountDetails();
  }, [getAccountDetails]);

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
      { path: routes.TASKS, element: <Tasks /> },
      { path: '*', element: <NotFound /> },
    ],
  },
];
