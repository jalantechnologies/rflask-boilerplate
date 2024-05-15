import React, { PropsWithChildren } from 'react';

const H3: React.FC<PropsWithChildren> = ({ children }) => (
  <h3 className="text-title-lg̦ font-bold text-black sm:text-title-xl2">
    {children}
  </h3>
);

export default H3;
