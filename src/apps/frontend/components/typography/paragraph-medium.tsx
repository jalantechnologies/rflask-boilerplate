import React, { PropsWithChildren, ReactNode } from 'react';

const ParagraphMedium: React.FC<PropsWithChildren<ReactNode>> = ({
  children,
}) => <p className="text-xl font-medium">{children}</p>;

export default ParagraphMedium;
