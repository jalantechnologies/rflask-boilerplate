import React, { PropsWithChildren } from 'react';

const LabelLarge: React.FC<PropsWithChildren> = ({ children }) => (
  <label className="text-lg font-medium text-black">{children}</label>
);

export default LabelLarge;
