import { AccessToken } from '../types';
import { JsonObject, Nullable } from '../types/common-types';

export const getAccessTokenFromStorage = (): Nullable<AccessToken> => {
  const token = localStorage.getItem('access-token');
  if (token) {
    return new AccessToken(JSON.parse(token) as JsonObject);
  }
  return null;
};

export const setAccessTokenToStorage = (token: AccessToken): void => {
  localStorage.setItem('access-token', JSON.stringify(token));
};

export const removeAccessTokenFromStorage = (): void => {
  localStorage.removeItem('access-token');
};
