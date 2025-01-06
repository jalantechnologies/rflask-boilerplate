import clsx from 'clsx';
import React, { PropsWithChildren } from 'react';

import styles from './flex.styles';
import ErrorBoundary from '../../error/ErrorBoundary';

interface FlexProps {
  alignItems?: string;
  direction?: string;
  flexWrap?: string;
  gap?: number;
  justifyContent?: string;
}

const Flex: React.FC<PropsWithChildren<FlexProps>> = ({
  alignItems = 'start',
  children,
  direction = 'row',
  flexWrap = 'nowrap',
  gap = '0',
  justifyContent = 'start',
}) => (
  <ErrorBoundary>
    <div
      className={clsx([
        styles.flex,
        styles.direction[direction],
        styles.justifyContent[justifyContent],
        styles.alignItems[alignItems],
        styles.flexWrap[flexWrap],
        styles.gap[gap],
      ])}
    >
      {children}
    </div>
  </ErrorBoundary>
);

export default Flex;
