import React, { PropsWithChildren, CSSProperties } from 'react';
import clsx from 'clsx'; 

interface H2Props extends PropsWithChildren {
  style?: CSSProperties;
  className?: string; 
}

const H2: React.FC<H2Props> = ({ children, style, className }) => (
  <h2
    className={clsx(
      'text-2xl font-bold text-black sm:text-title-xl2', 
      className
    )}
    style={style}
  >
    {children}
  </h2>
);

export default H2;
