import React from 'react';
import ReactDOM from 'react-dom';

import './satoshi.css';
import './style.css';

import App from './app.component';

document.addEventListener('DOMContentLoaded', () => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  ReactDOM.render(<App />, document.getElementById('app'));
});
