import React, { PropsWithChildren } from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

const AuthenticationPageLayout: React.FC<PropsWithChildren> = ({
  children,
}) => (
  <ErrorBoundary>
    <div className="rounded-sm border border-stroke shadow-default dark:border-strokedark dark:bg-boxdark">
      {children}
    </div>
  </ErrorBoundary>
);

export default AuthenticationPageLayout;
