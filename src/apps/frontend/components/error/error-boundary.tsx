import axios from 'axios';
import React, { Component, ErrorInfo, ReactNode } from 'react';

import { JsonObject } from '../../types/common-types';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    const errorData: JsonObject = {
      'error-name': error.name,
      'error-message': error.message,
      'error-info': errorInfo.componentStack,
    };
    axios.post('http://127.0.0.1:8080/client_logs', errorData);
  }

  public render() {
    if (this.state.hasError) {
      return <div>Sorry.. there was an error</div>;
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
