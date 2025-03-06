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
  startIcon?: React.ReactElement | string;
  endIcon?: React.ReactElement | string;
}

const ButtonClasses: Record<ButtonKind, string> = {
  [ButtonKind.PRIMARY]:
    'flex w-full items-center justify-center rounded-lg border bg-primary p-4 font-medium text-white transition active:bg-primary/80',
  [ButtonKind.SECONDARY]: 'inset-y-0 flex items-center',
  [ButtonKind.TERTIARY]:
    'bg-transparent text-center text-lg text-primary active:bg-transparent',
};

const DisabledClasses: Record<ButtonKind, string> = {
  [ButtonKind.PRIMARY]: 'cursor-not-allowed bg-primary/80',
  [ButtonKind.SECONDARY]: 'cursor-not-allowed',
  [ButtonKind.TERTIARY]: 'cursor-not-allowed text-slate-500',
};

const EnabledClasses: Record<ButtonKind, string> = {
  [ButtonKind.PRIMARY]: 'cursor-pointer hover:bg-primary/90',
  [ButtonKind.SECONDARY]: '',
  [ButtonKind.TERTIARY]: 'cursor-pointer',
};

const Button: React.FC<PropsWithChildren<ButtonProps>> = ({
  children,
  disabled,
  isLoading,
  onClick,
  type = ButtonType.BUTTON,
  kind = ButtonKind.PRIMARY,
  startIcon,
  endIcon,
}) => (
  <button
    className={clsx(
      ButtonClasses[kind],
      disabled || isLoading ? DisabledClasses[kind] : EnabledClasses[kind],
    )}
    disabled={disabled || isLoading}
    type={type}
    onClick={onClick}
  >
    {startIcon && (
      <span className="flex h-full min-w-6 items-center justify-center">
        {startIcon}
      </span>
    )}
    {isLoading ? <Spinner /> : children}
    {endIcon && (
      <span className="flex h-full min-w-6 items-center justify-center">
        {endIcon}
      </span>
    )}
  </button>
);

export default Button;
