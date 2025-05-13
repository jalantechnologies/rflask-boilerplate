import { datadogLogs } from '@datadog/browser-logs';
import { datadogRum } from '@datadog/browser-rum';
import useAsync from 'frontend/contexts/async.hook';
import getConfigValue from 'frontend/helpers/config';
import { AccountService } from 'frontend/services';
import { Account, ApiResponse, AsyncError } from 'frontend/types';
import { Nullable } from 'frontend/types/common-types';
import { getAccessTokenFromStorage } from 'frontend/utils/storage-util';
import React, { createContext, ReactNode, useContext } from 'react';

type AccountContextType = {
  accountDetails: Account;
  accountError: Nullable<AsyncError>;
  getAccountDetails: () => Promise<Nullable<Account>>;
  isAccountLoading: boolean;
};

type AccountContextProviderProps = {
  children: ReactNode;
};

const AccountContext = createContext<Nullable<AccountContextType>>(null);

const accountService = new AccountService();

export const useAccountContext = (): AccountContextType =>
  useContext(AccountContext) as AccountContextType;

const getAccountDetailsFn = async (): Promise<ApiResponse<Account>> => {
  const accessToken = getAccessTokenFromStorage();
  if (accessToken) {
    const accountDetails = await accountService.getAccountDetails(accessToken);

    const accountDetailsData = accountDetails?.data;

    if (getConfigValue('dataDog.enabled') === 'true' && accountDetailsData) {
      const dataDogAccount = {
        id: accountDetailsData.id,
        name: accountDetailsData.firstName,
        email: accountDetailsData.username,
        phone: accountDetailsData.phoneNumber,
      };

      datadogRum.setUser(dataDogAccount);
      datadogLogs.setAccount(dataDogAccount);
    }

    return accountDetails;
  }
  throw new Error('Access token not found');
};

export const AccountProvider: React.FC<AccountContextProviderProps> = ({
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
