import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { TestButton,ExpButton,STButton,SiFButton,StFButton,SLIMButton } from './Button';
import '../App.css';
import './ExpTools.css';



const Toolpage = () => {
  const [level, setLevel] = useState(0);
  const checkST = level==2 ? true: false;

  const fileInputRef=useRef("Empty");

  const inputFile = useRef(null) 
  const onButtonClick = () => {
    // `current` points to the mounted file input element
   inputFile.current.click();
  };
  
  function handleClick() {
    setButtonText('New text');
  }


  return (
    <div>
      <div className='tool-header'>
        <h1>Experiment</h1>
      </div>
      <div className="background-container">
        <div className="inner-container">
          <div>
            <div className="exp-titles">Workflow</div>
            <div className="exp-titles">Tool</div>
            <div className="exp-titles_2">Data</div>
            <div className="exp-titles">Run Experiment</div>
          </div>
        
          <div>
            <div className="inner-container-2">
              <div>
                <button level={1} onClick={() => setLevel("ST")} disabled={false} className={level=="ST" || level=="PW" || level=="MZ" || level=="DM" || level=="AC" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>Single-Tool</button>
                <button level={1} onClick={() => setLevel("PP")} disabled={true} className= {'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>PNNL PreProcessor</button>
              <div>
                </div>
                <button level={1} onClick={() => setLevel("SIF")} disabled={false} className={level=="SIF" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>Single Field</button>
                <button level={1} onClick={() => setLevel("PW")} className={level=="PW" || level=="STF" || level=="SIF" || level=="SLIM"? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>Proteowizard</button>
              </div>
              <div>
                <button level={1} onClick={() => setLevel("STF")} disabled={false} className={level=="STF" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>Stepped Field</button>
                <button level={1} onClick={() => setLevel("MZ")}  className={level=="MZ" || level=="STF" || level=="SIF" || level=="SLIM"? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>Mzmine</button>
              </div>
              <div>
                <button level={1} onClick={() => setLevel("SLIM")} disabled={false} className={level=="SLIM" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>SLIM</button>
                <button level={1} onClick={() => setLevel("DM")} disabled={level ==0 || level=="ST" || level=="DM" || level=="MZ" || level=="AC" || level=="PW"  ? false: true} className={level=="DM" ? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>DEIMoS</button>
              </div>
              <div>
                <button level={1} disabled={false} className='btn--new' buttonStyle='btn--outline' buttonSize='btn--large'></button>
                <button component="span" level={1} onClick={() => setLevel("AC")}  className={level=="AC" || level=="STF" || level=="SIF" || level=="SLIM"? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>AutoCCS</button>
              </div>
            </div>
            <div className="innest-container">

            </div>
            <div className="innest-container_2">
              <button level={1} onClick={() => {setLevel(0); handleClick();}}  disabled={true} className='btn--new_2' buttonStyle='btn--outline' buttonSize='btn--large'>Run Experiment{buttonText}</button>
            </div>
          </div>
        </div>
        <button onClick={()=>fileInputRef.current.click()}>
        Custom File Input Button
      </button>
      <input onChange={checkST} multiple={false} ref={fileInputRef} type='file'hidden/>
      <div>
      <input type='file' id='file' ref={inputFile} style={{display: 'none'}}/>
      <button onClick={onButtonClick}>Open file upload window </button>



      </div>
      </div>
    </div>
  );
};

// const Toolpage = () => {
//   const [level, setLevel] = useState(0);

//   const checkST = level==2 ? true: false;



//   return (
//     <div className="example">
//       <STButton className='btn' buttonStyle='btn--exppage' buttonSize='btn--large' onClick={() => setLevel(1)} >Single Tool{checkST}</STButton>
//       <STButton className='btn' buttonStyle='btn--exppage' buttonSize='btn--large'>
//       <button level={1} onClick={() => setLevel(1)} disabled={level !== 0} className='btn--new' buttonSize='btn--large'>
//         PNNL PreProcessor
//       </button></STButton>
//       <button level={1} onClick={() => setLevel(1)} disabled={level !== 0} className='btn--new' buttonStyle='btn--outline' buttonSize='btn--large'>PNNL PreProcessor</button>
//       <button level={2} onClick={() => setLevel(2)} disabled={level !== 1}>
//         Level 2
//       </button>
//       <button level={3} onClick={() => setLevel(0)} disabled={level !== 2}>
//         Level 3
//       </button>
//       <div>Level: {level}</div>
//     </div>
//   );
// };



export default Toolpage;