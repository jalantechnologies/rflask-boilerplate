import React from 'react';
import { Navigate } from 'react-router-dom';

import routes from '../constants/routes';
import { About } from '../pages';

export const publicRoutes = [
  { path: routes.ABOUT, element: <About /> },
  { path: '*', element: <Navigate to={routes.LOGIN} /> },
];

