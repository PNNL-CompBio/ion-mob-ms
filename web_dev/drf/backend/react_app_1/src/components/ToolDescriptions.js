import React from 'react';
import { Button } from './Button';
import '../App.css';
import './ToolDescriptions.css';



function ToolDescriptions() {
  return (
    <>
    <div className='tool-header'>
        <h1>Tool Descriptions</h1>
    </div>
        <div className='tool-container'>
            <h1>
            <a className='tool-title' target="_blank" href="https://pnnl-comp-mass-spec.github.io/PNNL-PreProcessor"> PNNL PreProcessor</a>  
            <div className='tool-description'>Sum frames and smooth raw data. (Unavailable)</div>
            </h1>
        </div>
        <div className='tool-container'>
            <h1>
            <a className='tool-title' target="_blank" href="https://proteowizard.sourceforge.io/"> ProteoWizard</a>  
            <div className='tool-description'>Convert preprocessed or raw data to mzML format.</div>
            </h1>
        </div>
        <div className='tool-container'>
            <h1>
            <a className='tool-title' target="_blank" href="https://github.com/mzmine/mzmine2"> mzMine2</a>  
            <div className='tool-description'>Detect features from mzML files.</div>
            </h1>
        </div>
        <div className='tool-container'>
            <h1>
            <a className='tool-title' target="_blank" href="https://github.com/pnnl/deimos"> DEIMoS</a>  
            <div className='tool-description'>Detect features and calculate collision cross-section values.</div>
            </h1>
        </div>
        <div className='tool-container'>
            <h1>
            <a className='tool-title' target="_blank" href="https://github.com/PNNL-Comp-Mass-Spec/AutoCCS"> AutoCCS</a>  
            <div className='tool-description'>Calculate collision corss section values from feature files using "standard" or "enhanced" methods.</div>
            </h1>
        </div>
        </>      
  );
}

export default ToolDescriptions;