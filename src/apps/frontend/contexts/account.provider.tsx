import React, {
  createContext,
  PropsWithChildren,
  ReactNode,
  useContext,
} from 'react';

import { AccountService } from '../services';
import { Account, ApiResponse, AsyncError } from '../types';

import useAsync from './async.hook';

type AccountContextType = {
  accountDetails: Account;
  accountError: AsyncError | undefined;
  getAccountDetails: () => Promise<Account | undefined>;
  isAccountLoading: boolean;
};

const AccountContext = createContext<AccountContextType | null>(null);

const accountService = new AccountService();

export const useAccountContext = (): AccountContextType =>
  useContext(AccountContext) as AccountContextType;

const getAccountDetailsFn = async (): Promise<ApiResponse<Account>> =>
  accountService.getAccountDetails();

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
