import React, { PropsWithChildren } from 'react';

const HeadingLarge: React.FC<PropsWithChildren> = ({ children }) => (
  <h2 className="text-[28px] font-semibold text-black">{children}</h2>
);

export default HeadingLarge;
