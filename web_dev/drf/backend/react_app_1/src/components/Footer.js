import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import { Button } from './Button';
import './Footer.css';


function Footer() {
  return (
    <>
    <div className='footer'>
        <div className='foot-item'>
        <a className='foot-item' target="_blank" href="https://github.com/PNNL-CompBio/ion-mob-ms"> Github Site</a>
        </div>
            <div className='foot-item'>
        <a className='foot-item' target="_blank" href="https://github.com/PNNL-CompBio/ion-mob-ms"> Documentation Site</a>  
        </div> 
        <div className='foot-item'>Contact</div>
        <div className='foot-item'>PNNL</div>
    </div>

    {/* <li className='foot-item'>
        <Link to ='/Documentation' className='foot-links'>
        MOOOOO  
        </Link>
    </li> */}
    </>
  );
}

export default Footer