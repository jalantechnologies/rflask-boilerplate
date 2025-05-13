import React, { ReactNode } from 'react';

export type ParagraphMediumProps = {
  children: ReactNode;
};

const ParagraphMedium: React.FC<ParagraphMediumProps> = ({ children }) => (
  <p className="font-medium text-bodydark2">{children}</p>
);

export default ParagraphMedium;
