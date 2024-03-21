import React, { createContext, PropsWithChildren, useContext } from 'react';

import { AuthService } from '../services';
import { AccessToken, ApiResponse, AsyncError } from '../types';

import useAsync from './async.hook';

type AuthContextType = {
  isSignupLoading: boolean;
  isUserAuthenticated: () => boolean;
  logout: () => void;
  signup: (
    firstName: string,
    lastName: string,
    username: string,
    password: string,
  ) => Promise<void>;
  signupError: AsyncError;
};

const AuthContext = createContext<AuthContextType | null>(null);

const authService = new AuthService();

export const useAuthContext = (): AuthContextType => useContext(AuthContext);

const signupFn = async (
  firstName: string,
  lastName: string,
  username: string,
  password: string,
): Promise<ApiResponse<void>> =>
  authService.signup(firstName, lastName, username, password);

const logoutFn = (): void => localStorage.removeItem('access-token');

const getAccessToken = (): AccessToken =>
  JSON.parse(localStorage.getItem('access-token')) as AccessToken;

const isUserAuthenticated = () => !!getAccessToken();

export const AuthProvider: React.FC<PropsWithChildren> = ({ children }) => {
  const {
    asyncCallback: signup,
    error: signupError,
    isLoading: isSignupLoading,
  } = useAsync(signupFn);

  return (
    <AuthContext.Provider
      value={{
        isSignupLoading,
        isUserAuthenticated,
        logout: logoutFn,
        signup,
        signupError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
