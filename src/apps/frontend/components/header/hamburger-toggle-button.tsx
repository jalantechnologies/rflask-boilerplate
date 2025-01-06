import React from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

type HamburgerToggleButtonProps = {
  isActive: boolean;
  onClick: (state: boolean) => void;
};

const HamburgerToggleButton: React.FC<HamburgerToggleButtonProps> = ({
  isActive,
  onClick,
}) => (
  <ErrorBoundary>
    <button
      aria-controls="sidebar"
      onClick={(e) => {
        e.stopPropagation();
        onClick(!isActive);
      }}
      className="block rounded-sm border border-stroke bg-white p-1.5 shadow-sm dark:border-strokedark dark:bg-boxdark lg:hidden"
    >
      <ErrorBoundary>
        <span className="relative block size-5.5 cursor-pointer">
          <ErrorBoundary>
            <span className="absolute right-0 block size-full">
              <ErrorBoundary>
                <span
                  className={`relative left-0 top-0 my-1 block h-0.5 w-0 rounded-sm bg-black delay-[0] duration-200 ease-in-out dark:bg-white ${
                    !isActive && '!w-full delay-200'
                  }`}
                ></span>
              </ErrorBoundary>
              <ErrorBoundary>
                <span
                  className={`relative left-0 top-0 my-1 block h-0.5 w-0 rounded-sm bg-black delay-150 duration-200 ease-in-out dark:bg-white ${
                    !isActive && '!w-full delay-300'
                  }`}
                ></span>
              </ErrorBoundary>
              <ErrorBoundary>
                <span
                  className={`relative left-0 top-0 my-1 block h-0.5 w-0 rounded-sm bg-black delay-200 duration-200 ease-in-out dark:bg-white ${
                    !isActive && '!w-full delay-500'
                  }`}
                ></span>
              </ErrorBoundary>
            </span>
          </ErrorBoundary>
          <ErrorBoundary>
            <span className="absolute right-0 size-full rotate-45">
              <ErrorBoundary>
                <span
                  className={`absolute left-2.5 top-0 block h-full w-0.5 rounded-sm bg-black delay-300 duration-200 ease-in-out dark:bg-white ${
                    !isActive && '!h-0 !delay-[0]'
                  }`}
                ></span>
              </ErrorBoundary>
              <ErrorBoundary>
                <span
                  className={`absolute left-0 top-2.5 block h-0.5 w-full rounded-sm bg-black delay-300 duration-200 ease-in-out dark:bg-white ${
                    !isActive && '!h-0 !delay-200'
                  }`}
                ></span>
              </ErrorBoundary>
            </span>
          </ErrorBoundary>
        </span>
      </ErrorBoundary>
    </button>
  </ErrorBoundary>
);

export default HamburgerToggleButton;
