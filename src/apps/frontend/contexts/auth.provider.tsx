import React, { createContext, PropsWithChildren, useContext } from 'react';

import { AuthService } from '../services';
import { AccessToken, ApiResponse, AsyncError } from '../types';

import useAsync from './async.hook';

type AuthContextType = {
  isLoginLoading: boolean;
  isSignupLoading: boolean;
  isUserAuthenticated: () => boolean;
  login: (username: string, password: string) => Promise<AccessToken>;
  loginError: AsyncError;
  loginResult: AccessToken;
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
): Promise<ApiResponse<void>> => authService.signup(firstName, lastName, username, password);

const loginFn = async (
  username: string,
  password: string,
): Promise<ApiResponse<AccessToken>> => {
  const result = await authService.login(username, password);
  if (result.data) {
    localStorage.setItem('access-token', JSON.stringify(result.data));
  }
  return result;
};

const logoutFn = (): void => localStorage.removeItem('access-token');

const getAccessToken = (): AccessToken => JSON.parse(localStorage.getItem('access-token')) as AccessToken;

const isUserAuthenticated = () => !!getAccessToken();

export const AuthProvider: React.FC<PropsWithChildren> = ({ children }) => {
  const {
    asyncCallback: signup,
    error: signupError,
    isLoading: isSignupLoading,
  } = useAsync(signupFn);

  const {
    isLoading: isLoginLoading,
    error: loginError,
    result: loginResult,
    asyncCallback: login,
  } = useAsync(loginFn);

  return (
    <AuthContext.Provider
      value={{
        isLoginLoading,
        isSignupLoading,
        isUserAuthenticated,
        login,
        loginError,
        loginResult,
        logout: logoutFn,
        signup,
        signupError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
