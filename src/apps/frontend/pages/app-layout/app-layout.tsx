import React, { PropsWithChildren } from 'react';

import { Header } from '../../components';
import Sidebar from '../../components/sidebar';
import ErrorBoundary from '../../error/ErrorBoundary';

export const AppLayout: React.FC<PropsWithChildren> = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);

  return (
    <ErrorBoundary>
      <div className="dark:bg-boxdark-2 dark:text-bodydark">
        <ErrorBoundary>
          <div className="flex h-screen overflow-hidden">
            {/* Sidebar */}
            <Sidebar
              isSidebarOpen={isSidebarOpen}
              setIsSidebarOpen={setIsSidebarOpen}
            />

            <ErrorBoundary>
              <div className="relative flex flex-1 flex-col">
                {/* Header */}
                <ErrorBoundary>
                  <Header
                    isSidebarOpen={isSidebarOpen}
                    setIsSidebarOpen={setIsSidebarOpen}
                  />
                </ErrorBoundary>

                {/* Main Content */}
                <ErrorBoundary>
                  <main>{children}</main>
                </ErrorBoundary>
              </div>
            </ErrorBoundary>
          </div>
        </ErrorBoundary>
      </div>
    </ErrorBoundary>
  );
};

export default AppLayout;
