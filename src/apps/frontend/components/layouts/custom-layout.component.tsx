import React from 'react';

import { LayoutConfig } from './layout-config';

interface CustomLayoutProps {
  layoutType: string; // The prompt code for the layout (e.g., "half-image", "full-form")
  children: React.ReactNode; // The form or content to be rendered inside the layout
}

export const CustomLayout: React.FC<CustomLayoutProps> = ({
  layoutType,
  children,
}) => {
  // Get the layout component based on the layoutType
  const LayoutComponent = LayoutConfig[layoutType] || LayoutConfig.default;

  return <LayoutComponent>{children}</LayoutComponent>;
};
