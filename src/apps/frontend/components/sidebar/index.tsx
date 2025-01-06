import React, { useRef } from 'react';

import routes from '../../constants/routes';
import ErrorBoundary from '../../error/ErrorBoundary';
import SidebarMenuItem from './sidebar-menu-item';

type SidebarProps = {
  isSidebarOpen: boolean;
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>;
};

const Sidebar: React.FC<SidebarProps> = ({
  isSidebarOpen,
  setIsSidebarOpen,
}) => {
  const trigger = useRef(null);
  const sidebar = useRef(null);

  return (
    <ErrorBoundary>
      <aside
        ref={sidebar}
        className={`absolute left-0 top-0 z-9999 flex h-screen w-72.5 flex-col overflow-y-hidden bg-black duration-300 ease-linear dark:bg-boxdark lg:static lg:translate-x-0 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* <!-- SIDEBAR HEADER --> */}
        <ErrorBoundary>
          <div className="flex items-center justify-end gap-2 px-6 py-5.5 lg:py-6.5">
            <ErrorBoundary>
              <button
                ref={trigger}
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                aria-controls="sidebar"
                aria-expanded={isSidebarOpen}
                className="block lg:hidden"
              >
                <ErrorBoundary>
                  <img
                    src="/assets/img/icon/sidebar-arrow-icon.svg"
                    alt="arrow icon"
                  />
                </ErrorBoundary>
              </button>
            </ErrorBoundary>
          </div>
        </ErrorBoundary>

        {/* <!-- SIDEBAR MENU --> */}
        <ErrorBoundary>
          <div className="flex flex-col overflow-y-auto duration-300 ease-linear">
            <ErrorBoundary>
              <nav className="p-2 lg:px-6">
                <ErrorBoundary>
                  <h3 className="mb-2 ml-4 mt-4 text-sm font-semibold text-bodydark2">
                    MENU
                  </h3>
                </ErrorBoundary>
                <ErrorBoundary>
                  <ul className="mb-6 flex flex-col gap-1.5">
                    <ErrorBoundary>
                      <SidebarMenuItem
                        iconPath="/assets/img/icon/dashboard-sidebar-icon.svg"
                        path={routes.DASHBOARD}
                        setIsSidebarOpen={setIsSidebarOpen}
                        title="Dashboard"
                      />
                    </ErrorBoundary>
                    <ErrorBoundary>
                      <SidebarMenuItem
                        iconPath="/assets/img/icon/tasks-sidebar-icon.svg"
                        path={routes.TASKS}
                        setIsSidebarOpen={setIsSidebarOpen}
                        title="Tasks"
                      />
                    </ErrorBoundary>
                  </ul>
                </ErrorBoundary>
              </nav>
            </ErrorBoundary>
          </div>
        </ErrorBoundary>
      </aside>
    </ErrorBoundary>
  );
};

export default Sidebar;
