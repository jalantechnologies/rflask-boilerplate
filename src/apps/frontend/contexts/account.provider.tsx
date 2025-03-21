import React, {
  createContext,
  PropsWithChildren,
  ReactNode,
  useContext,
} from 'react';

import { AccountService } from '../services';
import { Account, ApiResponse, AsyncError } from '../types';
import { Nullable } from '../types/common-types';
import { getAccessTokenFromStorage } from '../utils/storage-util';

import useAsync from './async.hook';

type AccountContextType = {
  accountDetails: Account;
  accountError: Nullable<AsyncError>;
  getAccountDetails: () => Promise<Nullable<Account>>;
  isAccountLoading: boolean;
};

const AccountContext = createContext<Nullable<AccountContextType>>(null);

const accountService = new AccountService();

export const useAccountContext = (): AccountContextType =>
  useContext(AccountContext) as AccountContextType;

const getAccountDetailsFn = async (): Promise<ApiResponse<Account>> => {
  const accessToken = getAccessTokenFromStorage();
  if (accessToken) {
    return accountService.getAccountDetails(accessToken);
  }
  throw new Error('Access token not found');
};

export const AccountProvider: React.FC<PropsWithChildren<ReactNode>> = ({
  children,
}) => {
  const {
    isLoading: isAccountLoading,
    error: accountError,
    result: accountDetails,
    asyncCallback: getAccountDetails,
  } = useAsync(getAccountDetailsFn);

  return (
    <AccountContext.Provider
      value={{
        accountDetails: new Account({ ...accountDetails }), // creating an instance to access its methods
        accountError,
        getAccountDetails,
        isAccountLoading,
      }}
    >
      {children}
    </AccountContext.Provider>
  );
};
