import React, { PropsWithChildren, ReactNode } from 'react';

const ParagraphMedium: React.FC<PropsWithChildren<ReactNode>> = ({
  children,
}) => <p className="font-medium text-bodydark2">{children}</p>;

export default ParagraphMedium;
