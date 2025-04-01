import styles from 'frontend/components/tooltip/tooltip.styles';
import React, { useState, PropsWithChildren } from 'react';

interface TooltipProps {
  content: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

const Tooltip: React.FC<PropsWithChildren<TooltipProps>> = ({
  content,
  children,
  position = 'top',
}) => {
  const [visible, setVisible] = useState(false);

  return (
    <div
      className={styles.container}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      <div
        className={`${styles.tooltip} ${visible ? styles.visible : styles.hidden} ${styles.positions[position]}`}
        role="tooltip"
      >
        {content}
        <div className="tooltip-arrow" data-popper-arrow></div>
      </div>
    </div>
  );
};

export default Tooltip;
