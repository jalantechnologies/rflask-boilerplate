import React from 'react';

interface TextAreaProps {
  cols: number;
  rows: number;
  value: string;
  name: string;
  placeholder: string;
  disabled?: boolean;
  testId?: string;
  onBlur?: React.FocusEventHandler<HTMLTextAreaElement>;
  onChange: React.ChangeEventHandler<HTMLTextAreaElement>;
}

const TextArea: React.FC<TextAreaProps> = ({
  cols,
  rows,
  value,
  name,
  placeholder,
  disabled = false,
  testId,
  onBlur,
  onChange,
}) => {
  return (
    <textarea
      cols={cols}
      rows={rows}
      value={value}
      name={name}
      placeholder={placeholder}
      disabled={disabled}
      onBlur={onBlur}
      onChange={onChange}
      data-testid={testId}
      className={`w-full rounded-sm border px-4.5 py-3 text-black focus:border-primary focus-visible:outline-none border-stroke`}
    />
  );
};

export default TextArea;
