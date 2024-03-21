import React from 'react';
import { Navigate } from 'react-router-dom';

import routes from '../constants/routes';
import { About, Signup } from '../pages';

export const publicRoutes = [
  {
    path: routes.SIGNUP,
    element: <Signup />,
  },
  { path: routes.ABOUT, element: <About /> },
  { path: '*', element: <Navigate to={routes.SIGNUP} /> },
];
