import React, { PropsWithChildren } from 'react';

const H3: React.FC<PropsWithChildren> = ({ children }) => (
  <h3 className=" font-bold text-black ">
    {children}
  </h3>
);

export default H3;
