import React from 'react';
import { useRoutes } from 'react-router-dom';

import { useAuthContext } from '../contexts';

import { protectedRoutes } from './protected';
import { publicRoutes } from './public';

export const AppRoutes = () => {
  const { isUserAuthenticated } = useAuthContext();

  const routes = isUserAuthenticated() ? protectedRoutes : publicRoutes;

  const element = useRoutes([...routes, ...publicRoutes]);

  return <>{element}</>;
};
