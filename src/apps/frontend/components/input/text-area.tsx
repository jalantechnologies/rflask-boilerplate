import React from 'react';

interface TextAreaProps {
  cols: number;
  disabled?: boolean;
  name: string;
  onBlur?: React.FocusEventHandler<HTMLTextAreaElement>;
  onChange: React.ChangeEventHandler<HTMLTextAreaElement>;
  placeholder: string;
  rows: number;
  testId?: string;
  value: string;
}

const TextArea: React.FC<TextAreaProps> = ({
  cols,
  disabled = false,
  name,
  onBlur,
  onChange,
  placeholder,
  rows,
  testId,
  value,
}) => {
  return (
    <textarea
      className={`w-full rounded-sm border px-4.5 py-3 text-black focus:border-primary focus-visible:outline-none border-stroke`}
      cols={cols}
      data-testid={testId}
      disabled={disabled}
      name={name}
      onBlur={onBlur}
      onChange={onChange}
      placeholder={placeholder}
      rows={rows}
      value={value}
    />
  );
};

export default TextArea;
