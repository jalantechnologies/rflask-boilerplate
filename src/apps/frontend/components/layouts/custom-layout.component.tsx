import { LayoutConfig, LayoutType } from 'frontend/components/layouts/layout-config';
import React from 'react';

interface CustomLayoutProps {
  layoutType?: LayoutType;
  children: React.ReactNode;
}

export const CustomLayout: React.FC<CustomLayoutProps> = ({
  layoutType = LayoutType.Default,
  children,
}) => {
  const LayoutComponent = LayoutConfig[layoutType] || LayoutConfig.default;

  return <LayoutComponent>{children}</LayoutComponent>;
};
