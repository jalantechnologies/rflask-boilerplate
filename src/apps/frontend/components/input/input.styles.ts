const styles = {
  inputContainer: `
    w-full
    rounded-lg
    border
    bg-white
    py-4
    px-4
    outline-none
    focus:border-primary
    focus-visible:shadow-none
  `,
  input: `
    flex-1
    w-full
    outline-none
    [appearance:textfield]
    [&::-webkit-inner-spin-button]:appearance-none
  `,
  border: {
    errorState: 'border-red-500',
    normalState: 'border-stroke',
  },
  textAlign: {
    center: 'text-center',
    left: 'text-left',
    right: 'text-right',
  },
};

export default styles;
