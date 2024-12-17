import React from 'react';
import Input from '.'; // Assuming Input is a custom component

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
        type="date" // The native date picker
      />
    </div>
  );
};

export default DateInput;
