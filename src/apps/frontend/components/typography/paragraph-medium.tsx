import React, { PropsWithChildren } from 'react';

const ParagraphMedium: React.FC<PropsWithChildren> = ({
  children,
}) => (
  <p className="text-xl font-medium">
    {children}
  </p>
);

export default ParagraphMedium;
