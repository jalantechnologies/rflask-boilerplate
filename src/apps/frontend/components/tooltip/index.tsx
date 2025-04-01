import React, { useState, PropsWithChildren } from 'react';

interface TooltipProps {
  content: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

const Tooltip: React.FC<PropsWithChildren<TooltipProps>> = ({
  content,
  children,
  position = 'top',
}) => {
  const [visible, setVisible] = useState(false);

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      <div
        className={`absolute z-10 rounded-lg bg-black px-3 py-2 text-sm font-medium text-white shadow-lg transition-opacity duration-300 
          ${visible ? 'opacity-100' : 'invisible opacity-0'} 
          ${position === 'top' ? 'bottom-full left-1/2 mb-2 -translate-x-1/2' : ''}
          ${position === 'bottom' ? 'left-1/2 top-full mt-2 -translate-x-1/2' : ''}
          ${position === 'left' ? 'right-full top-1/2 mr-2 -translate-y-1/2' : ''}
          ${position === 'right' ? 'left-full top-1/2 ml-2 -translate-y-1/2' : ''}`}
        role="tooltip"
      >
        {content}
        <div className="tooltip-arrow" data-popper-arrow></div>
      </div>
    </div>
  );
};

export default Tooltip;
