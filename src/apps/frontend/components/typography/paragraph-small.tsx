import React, { PropsWithChildren } from 'react';

const ParagraphSmall: React.FC<PropsWithChildren> = ({ children }) => (
  <p className="text-base font-medium">{children}</p>
);

export default ParagraphSmall;
