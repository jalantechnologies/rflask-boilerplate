import React from 'react';
import ReactDOM from 'react-dom/client';

import './satoshi.css';
import './style.css';

import App from './app.component';

const rootElement = document.getElementById('app');

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<App />);
}
