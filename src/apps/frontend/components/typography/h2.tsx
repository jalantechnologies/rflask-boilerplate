import React, { PropsWithChildren, ReactNode } from 'react';

const H2: React.FC<PropsWithChildren<ReactNode>> = ({ children }) => (
  <h2 className="text-title-xl2 font-bold text-black">{children}</h2>
);

export default H2;
