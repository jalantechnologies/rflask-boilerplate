import clsx from 'clsx';
import styles from 'frontend/components/flex/flex-item.styles';
import React, { PropsWithChildren } from 'react';

interface FlexItemProps {
  alignSelf?: keyof typeof styles.alignSelf;
  flex?: keyof typeof styles.flex;
  justifySelf?: keyof typeof styles.justifySelf;
  order?: keyof typeof styles.order;
}

const FlexItem: React.FC<PropsWithChildren<FlexItemProps>> = ({
  alignSelf = 'auto',
  children,
  flex = 'flexAuto',
  justifySelf = 'auto',
  order = 'none',
}) => (
  <div
    className={clsx([
      styles.alignSelf[alignSelf],
      styles.flex[flex],
      styles.justifySelf[justifySelf],
      styles.order[order],
    ])}
  >
    {children}
  </div>
);

export default FlexItem;
