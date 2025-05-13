import React, { ReactNode } from 'react';

type H2Props = {
  children: ReactNode;
};

const H2: React.FC<H2Props> = ({ children }) => (
  <h2 className="self-start pl-7 text-title-xl2 font-bold text-black">
    {children}
  </h2>
);

export default H2;
