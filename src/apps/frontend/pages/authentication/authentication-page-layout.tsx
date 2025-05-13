import React, { ReactNode } from 'react';

type AuthenticationPageLayoutProps = {
  children: ReactNode;
};

const AuthenticationPageLayout: React.FC<AuthenticationPageLayoutProps> = ({
  children,
}) => (
  <div className="rounded-sm border border-stroke shadow-default dark:border-strokedark dark:bg-boxdark">
    {children}
  </div>
);

export default AuthenticationPageLayout;
