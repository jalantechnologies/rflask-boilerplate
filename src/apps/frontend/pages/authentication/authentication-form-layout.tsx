import React from 'react';

import { CustomLayout } from '../../components/layouts/custom-layout.component';
import { LayoutType } from '../../components/layouts/layout-config';

interface AuthenticationFormLayoutProps {
  children: React.ReactNode;
  layoutType?: LayoutType;
}

const AuthenticationFormLayout: React.FC<AuthenticationFormLayoutProps> = ({
  children,
  layoutType = LayoutType.Default,
}) => (
  <CustomLayout layoutType={layoutType}>
    <div className="flex h-auto min-h-[70vh] items-center justify-center p-4 md:min-h-[50vh] lg:min-h-[60vh]">
      <div className="w-full rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-boxdark sm:p-4 md:w-full xl:w-full">
        {children}
      </div>
    </div>
  </CustomLayout>
);

export default AuthenticationFormLayout;
