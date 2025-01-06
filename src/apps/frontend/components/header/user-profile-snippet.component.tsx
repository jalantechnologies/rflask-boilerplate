import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';

import { Account } from '../../types';

import UserMenuDropdown from './user-menu-dropdown.component';

import { UserMenuDropdownItem } from '.';
import ErrorBoundary from '../../error/ErrorBoundary';

interface DropdownUserProps {
  account: Account;
  userMenuDropdownItems: UserMenuDropdownItem[];
}

const UserProfileSnippet: React.FC<DropdownUserProps> = ({
  account,
  userMenuDropdownItems,
}) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const trigger = useRef<HTMLAnchorElement>(null);
  const dropdown = useRef<HTMLDivElement>(null);

  // close on click outside
  useEffect(() => {
    const clickHandler = (event: MouseEvent) => {
      const targetNode = event.target as Node;
      if (!dropdown.current) return;
      if (
        !dropdownOpen ||
        dropdown.current.contains(targetNode) ||
        trigger.current.contains(targetNode)
      )
        return;
      setDropdownOpen(false);
    };
    document.addEventListener('click', clickHandler);
    return () => document.removeEventListener('click', clickHandler);
  }, [dropdownOpen]);

  // close if the esc key is pressed
  useEffect(() => {
    const keyHandler = ({ key }: KeyboardEvent) => {
      if (!dropdownOpen || key !== 'Escape') return;
      setDropdownOpen(false);
    };
    document.addEventListener('keydown', keyHandler);
    return () => document.removeEventListener('keydown', keyHandler);
  }, [dropdownOpen]);

  return (
    <ErrorBoundary>
      <div className="relative">
        <ErrorBoundary>
          <Link
            ref={trigger}
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-4"
            to="#"
          >
            <ErrorBoundary>
              <span className="hidden text-right lg:block">
                <ErrorBoundary>
                  <span className="block text-sm font-medium text-black dark:text-white">
                    {account.displayName()}
                  </span>
                </ErrorBoundary>
                <ErrorBoundary>
                  <span className="block text-xs">User</span>
                </ErrorBoundary>
              </span>
            </ErrorBoundary>

            <ErrorBoundary>
              <span className="size-12 rounded-full">
                <img src="/assets/img/user.png" alt="User" />
              </span>
            </ErrorBoundary>

            <ErrorBoundary>
              <img
                className="hidden fill-current opacity-50 sm:block"
                src="/assets/img/icon/drop-down-arrow.svg"
                alt="dropdown icon"
              />
            </ErrorBoundary>
          </Link>
        </ErrorBoundary>

        <ErrorBoundary>
          <UserMenuDropdown
            dropdownOpen={dropdownOpen}
            dropdownRef={dropdown}
            setDropdownOpen={setDropdownOpen}
            userMenuDropdownItems={userMenuDropdownItems}
          />
        </ErrorBoundary>
      </div>
    </ErrorBoundary>
  );
};

export default UserProfileSnippet;
