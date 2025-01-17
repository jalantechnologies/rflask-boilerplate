import React, { PropsWithChildren, ReactNode } from 'react';

const AuthenticationPageLayout: React.FC<PropsWithChildren<ReactNode>> = ({
  children,
}) => (
  <div className="rounded-sm border border-stroke shadow-default dark:border-strokedark dark:bg-boxdark">
    {children}
  </div>
);

export default AuthenticationPageLayout;
