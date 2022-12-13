import React from 'react';
import { Link } from 'react-router-dom';
import { ExpButton,STButton,SiFButton,StFButton,SLIMButton } from './Button';
import '../App.css';
import './ExperimentMain.css';



function ExpSLIM() {
  return (
    <>
    <div className='exp-header'>
        <h1>Experiment</h1>
    </div>  
        <div className='exp-container'>
            <div className='exp-title'>SLIM Page</div>

        </div>

        </>      
  );
}


export default ExpSLIM;