import React from 'react';

interface TextAreaProps {
  disabled: boolean;
  error: string;
  name: string;
  placeholder: string;
  rows: number;
}

const TextArea: React.FC<TextAreaProps> = ({
  disabled,
  error,
  name,
  placeholder,
  rows = 2,
}) => (
  <textarea
    rows={rows}
    placeholder={placeholder}
    className={`w-full rounded-lg border border-stroke bg-white px-4 py-2 text-black  ${
      error && 'border-red'
    }`}
    disabled={disabled}
    name={name}
  />
);

export default TextArea;
