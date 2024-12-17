const constant = {
  TITLE_MIN_LENGTH: 5,
  TITLE_VALIDATION_ERROR: 'Title must be at least 5 characters long.',
  DESCRIPTION_MIN_LENGTH: 10,
  DESCRIPTION_VALIDATION_ERROR: 'Description must be at least 10 characters long.',
  TYPE_VALIDATION_ERROR: 'Type must be one of: Official, Personal, or Hobby.',
  DUE_DATE_VALIDATION_ERROR: 'Due date must be in the future.',

  DEFAULT_ERROR_HTTP_STATUS_CODE: 500,
  EMAIL_VALIDATION_ERROR: 'Please enter a valid email',
  FIRST_NAME_MIN_LENGTH: 1,
  FIRST_NAME_VALIDATION_ERROR: 'Please specify your first name',
  LAST_NAME_MIN_LENGTH: 1,
  LAST_NAME_VALIDATION_ERROR: 'Please specify your last name',
  OTP_INPUT_MAX_LENGTH: 2,
  OTP_LENGTH: 4,
  PASSWORD_MATCH_VALIDATION_ERROR:
    "The confirmed password doesn't match the chosen password.",
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_VALIDATION_ERROR: 'Please enter at least 8 characters long password',
  PHONE_VALIDATION_ERROR: 'Please enter a valid phone number',
  SEND_OTP_DELAY_IN_MS: 60_000,
  TOASTER_AUTO_HIDE_DURATION: 3000,
};

export default constant;
