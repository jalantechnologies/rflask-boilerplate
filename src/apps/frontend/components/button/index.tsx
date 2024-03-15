import clsx from 'clsx';
import React, { PropsWithChildren } from 'react';

import { ButtonKind, ButtonType } from '../../types/button';
import Spinner from '../spinner/spinner';

import styles from './button.styles';

interface ButtonProps {
  disabled?: boolean;
  isLoading?: boolean;
  onClick?: (e) => void;
  type?: ButtonType;
  kind?: ButtonKind;
}

const Button: React.FC<PropsWithChildren<ButtonProps>> = ({
  children,
  disabled,
  isLoading,
  onClick,
  type = ButtonType.BUTTON,
  kind = ButtonKind.PRIMARY,
}) => {
  const content = isLoading && kind === ButtonKind.PRIMARY ? <Spinner /> : children;

  return (
    <button
      className={clsx([
        styles.kind[kind].base,
        (disabled || isLoading) ? styles.kind[kind].disableState : styles.kind[kind].enableState,
      ])}
      disabled={disabled || isLoading}
      type={type}
      onClick={onClick}
    >
      {content}
    </button>
  );
};

export default Button;
