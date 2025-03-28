import 'frontend/satoshi.css';
import 'frontend/style.css';

import App from 'frontend/app.component';
import React from 'react';
import ReactDOM from 'react-dom';

document.addEventListener('DOMContentLoaded', () => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  ReactDOM.render(<App />, document.getElementById('app'));
});
