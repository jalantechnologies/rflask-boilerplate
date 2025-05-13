import { Header } from 'frontend/components';
import Sidebar from 'frontend/components/sidebar';
import React, { ReactNode } from 'react';

type AppLayoutProps = {
  children: ReactNode;
};

export const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
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
