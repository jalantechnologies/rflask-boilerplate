import { Header } from 'frontend/components';
import Sidebar from 'frontend/components/sidebar';
import React, { PropsWithChildren, ReactNode } from 'react';

export const AppLayout: React.FC<PropsWithChildren<ReactNode>> = ({
  children,
}) => {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);

  return (
    <div className="dark:bg-boxdark-2 dark:text-bodydark">
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          isSidebarOpen={isSidebarOpen}
          setIsSidebarOpen={setIsSidebarOpen}
        />

        <div className="relative flex flex-1 flex-col">
          {/* Header */}
          <Header
            isSidebarOpen={isSidebarOpen}
            setIsSidebarOpen={setIsSidebarOpen}
          />

          {/* Main Content */}
          <main>{children}</main>
        </div>
      </div>
    </div>
  );
};

export default AppLayout;
