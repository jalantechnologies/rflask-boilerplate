import clsx from 'clsx';
import React, { PropsWithChildren } from 'react';

import { ButtonKind, ButtonType } from '../../types/button';
import Spinner from '../spinner/spinner';

interface ButtonProps {
  disabled?: boolean;
  isLoading?: boolean;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
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
  const content =
    isLoading && kind === ButtonKind.PRIMARY ? <Spinner /> : children;

  return (
    <button
      className={clsx(
        // Primary button
        kind === ButtonKind.PRIMARY &&
          'flex w-full items-center justify-center rounded-lg border bg-primary p-4 font-medium text-white transition active:bg-primary/80',
        // Secondary button
        kind === ButtonKind.SECONDARY && 'inset-y-0 flex items-center',
        // Tertiary button
        kind === ButtonKind.TERTIARY &&
          'bg-transparent text-center text-lg text-primary active:bg-transparent',
        // Disabled or loading states
        (disabled || isLoading) && 'cursor-not-allowed bg-primary/80',
        !disabled && !isLoading && 'cursor-pointer hover:bg-primary/90',
        kind === ButtonKind.TERTIARY &&
          disabled &&
          'cursor-not-allowed text-slate-500',
        kind === ButtonKind.TERTIARY && !disabled && 'cursor-pointer',
      )}
      disabled={disabled || isLoading}
      type={type}
      onClick={onClick}
    >
      {content}
    </button>
  );
};

export default Button;
