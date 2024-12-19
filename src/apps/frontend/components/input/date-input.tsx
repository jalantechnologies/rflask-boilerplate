import React from 'react';
import Input from '.';

interface DateInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  error: string;
  name: string;
  placeholder: string;
  testId?: string;
}

const DateInput: React.FC<DateInputProps> = ({
  error,
  name,
  placeholder,
  testId,
  ...props
}) => {
  return (
    <div>
      <Input
        data-testid={testId || 'date-input'}
        {...props}
        error={error}
        name={name}
        placeholder={placeholder}
        type="date"
      />
    </div>
  );
};

export default DateInput;
