// src/apps/frontend/components/layout/horizontal-stack-layout.tsx
import React, { PropsWithChildren } from 'react';
import clsx from 'clsx';

interface HorizontalStackLayoutProps {
  gap?: number;
  className?: string;
  align?: 'start' | 'center' | 'end';
}

const HorizontalStackLayout: React.FC<
  PropsWithChildren<HorizontalStackLayoutProps>
> = ({ children, gap = 2, className, align = 'center' }) => (
  <div
    className={clsx('flex w-full', `gap-${gap}`, `items-${align}`, className)}
  >
    {children}
  </div>
);

export default HorizontalStackLayout;
