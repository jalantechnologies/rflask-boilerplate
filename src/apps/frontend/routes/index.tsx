import { useAuthContext } from 'frontend/contexts';
import { protectedRoutes } from 'frontend/routes/protected';
import { publicRoutes } from 'frontend/routes/public';
import React from 'react';
import { useRoutes } from 'react-router-dom';

export const AppRoutes = () => {
  const { isUserAuthenticated } = useAuthContext();

  const routes = isUserAuthenticated() ? protectedRoutes : publicRoutes;

  const element = useRoutes([...routes, ...publicRoutes]);

  return <>{element}</>;
};
