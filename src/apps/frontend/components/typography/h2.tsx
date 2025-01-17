import React, { PropsWithChildren, ReactNode } from 'react';

const H2: React.FC<PropsWithChildren<ReactNode>> = ({ children }) => (
  <h2 className="text-2xl font-bold text-black sm:text-title-xl2">
    {children}
  </h2>
);

export default H2;
