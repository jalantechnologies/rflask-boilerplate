import React from 'react';
import ReactDOM from 'react-dom';

import './satoshi.css';
import './style.css';
import App from './app.component';

const container = document.getElementById('app');

// eslint-disable-next-line @typescript-eslint/no-unsafe-call
ReactDOM.createRoot(container).render(<App />);
