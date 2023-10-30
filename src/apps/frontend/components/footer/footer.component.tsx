import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer(): React.ReactElement {
  return (
    <div className='container'>
      <div>
        <Link to='/about'>About Us</Link>
      </div>
      <div className='text-muted'>
        &#169; Jalan Technology Consulting, 2022
      </div>
    </div>
  );
}
