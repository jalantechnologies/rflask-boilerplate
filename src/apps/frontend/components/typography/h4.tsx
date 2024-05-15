import React, { PropsWithChildren } from 'react';

const H4: React.FC<PropsWithChildren> = ({ children }) => (
  <h4 className=" text-lg font-bold text-black">
    {children}
  </h4>
);

export default H4;
