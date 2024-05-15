import clsx from 'clsx';
import React, { PropsWithChildren } from 'react';

import { ButtonKind, ButtonType } from '../../types/button';
import Spinner from '../spinner/spinner';

import styles from './button.styles';
import HorizontalStackLayout from '../layouts/horizontal-stack-layout';

interface ButtonProps {
  disabled?: boolean;
  fullWidth?: boolean;
  isLoading?: boolean;
  onBlur?: (e) => void;
  onClick?: (e) => void;
  startIcon?: React.ReactElement | string;
  type?: ButtonType;
  kind?: ButtonKind;
}

const Button: React.FC<PropsWithChildren<ButtonProps>> = ({
  children,
  disabled,
  fullWidth,
  isLoading,
  onBlur,
  onClick,
  startIcon,
  type = ButtonType.BUTTON,
  kind = ButtonKind.PRIMARY,
}) => {
  const content =
    isLoading && kind === ButtonKind.PRIMARY ? <Spinner /> : children;

  return (
    <button
      className={clsx([
        styles.kind[kind].base,
        disabled || isLoading
          ? styles.kind[kind].disableState
          : styles.kind[kind].enableState,
        fullWidth && 'w-full',
      ])}
      disabled={disabled || isLoading}
      type={type}
      onBlur={onBlur}
      onClick={onClick}
    >
      <HorizontalStackLayout gap={2}>
        {startIcon}
        {content}
      </HorizontalStackLayout>
    </button>
  );
};

export default Button;
