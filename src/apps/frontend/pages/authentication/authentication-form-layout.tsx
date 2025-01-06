import React, { PropsWithChildren } from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

const AuthenticationFormLayout: React.FC<PropsWithChildren> = ({
  children,
}) => (
  <ErrorBoundary>
    <div className="flex min-h-screen flex-wrap items-center justify-center p-4 md:p-6 2xl:p-10">
      <ErrorBoundary>
        <div className="w-full rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-boxdark sm:p-12.5 md:w-4/5 xl:w-2/5">
          {children}
        </div>
      </ErrorBoundary>
    </div>
  </ErrorBoundary>
);

export default AuthenticationFormLayout;
