import clsx from 'clsx';
import React, { PropsWithChildren } from 'react';

import styles from './flex.styles';

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
);

export default Flex;
