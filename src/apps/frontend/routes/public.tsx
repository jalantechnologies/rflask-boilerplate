import React from 'react';
import { Navigate } from 'react-router-dom';

import routes from '../constants/routes';
import { About, Signup } from '../pages';
import Login from '../pages/login';

export const publicRoutes = [
  {
    path: routes.LOGIN,
    element: <Login />,
  },
  {
    path: routes.SIGNUP,
    element: <Signup />,
  },
  { path: routes.ABOUT, element: <About /> },
  { path: '*', element: <Navigate to={routes.LOGIN} /> },
];
