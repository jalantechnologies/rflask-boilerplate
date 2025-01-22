import React, { PropsWithChildren } from 'react';

const H2Header: React.FC<PropsWithChildren> = ({ children }) => (
  <h2 className="mb-6 text-center text-3xl font-bold text-boxdark">
    {children}
  </h2>
);

export default H2Header;
