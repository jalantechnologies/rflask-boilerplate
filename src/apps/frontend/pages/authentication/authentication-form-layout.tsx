import React from 'react';

import { CustomLayout } from '../../components/layouts/custom-layout.component';

interface AuthenticationFormLayoutProps {
  children: React.ReactNode;
  layoutType?: string;
}

const AuthenticationFormLayout: React.FC<AuthenticationFormLayoutProps> = ({
  children,
  layoutType = 'background-image', // The prompt code for the layout (e.g., "half-image", "full-form","background-image")
}) => (
  <CustomLayout layoutType={layoutType}>
    <div className="flex min-h-screen flex-wrap items-start justify-center p-4 md:p-6 2xl:p-10">
      <div className="w-full rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-boxdark sm:p-4 md:w-full xl:w-full">
        {children}
      </div>
    </div>
  </CustomLayout>
);

export default AuthenticationFormLayout;
