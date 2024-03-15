import clsx from 'clsx';
import React, { PropsWithChildren } from 'react';

import styles from './flex-item.styles';

interface FlexItemProps {
  alignSelf?: 'auto' | 'flexStart' | 'flexEnd' | 'center' | 'baseline' | 'stretch';
  flex?: 'flex1' | 'flexAuto' | 'flexInitial' | 'flexNone' | 'grow0' | 'grow' | 'shrink0' | 'shrink';
  justifySelf?: 'auto' | 'start' | 'end' | 'center' | 'stretch';
  order?: 'first' | 'last' | 'none' | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
}

const FlexItem: React.FC<PropsWithChildren<FlexItemProps>> = ({
  alignSelf,
  children,
  flex,
  justifySelf,
  order,
}) => (
    <div className={clsx([
      styles.alignSelf[alignSelf],
      styles.flex[flex],
      styles.justifySelf[justifySelf],
      styles.order[order],
    ])}>
      {children}
    </div>
);

export default FlexItem;
