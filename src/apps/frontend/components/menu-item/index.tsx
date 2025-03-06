import React, { useState } from 'react';

import { ButtonKind } from '../../types/button';
import Button from '../button';

const MenuItem: React.FC = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div className="relative flex">
      <Button onClick={() => setIsOpen(!isOpen)} kind={ButtonKind.TERTIARY}>
        <img src="assets/img/icon/ellipsis-icon.svg" alt="Ellipsis Icon" />
      </Button>
      <div
        onFocus={() => setIsOpen(true)}
        onBlur={() => setIsOpen(false)}
        className={`absolute right-0 top-full z-40 w-40 space-y-1 rounded-sm border border-stroke bg-white p-1.5 shadow-default ${
          isOpen ? 'block' : 'hidden'
        }`}
      >
        {children}
      </div>
    </div>
  );
};

export default MenuItem;
