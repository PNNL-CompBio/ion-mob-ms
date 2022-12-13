import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { TestButton,ExpButton,STButton,SiFButton,StFButton,SLIMButton } from './Button';
import '../App.css';
import './ExperimentMain.css';
import { useStateWithCallback } from './useStateWithCallback';
import axios from 'axios';
import * as Minio from "minio";


// Experiment Button
// This will check if all files are present, then will run if so.
const Experiment = () => {
  const [buttonText, setButtonText] = useState('Run Experiment');
  function handleClick() {
    setButtonText('Choose Files before Running Experiment.')
    if (document.getElementById('EXP_name').value != '') {
      if (level == "PW" && document.getElementById('PP_file').files[0]) {
      Upload_Files()
      setButtonText('Experiment Running') }
      if (level == "MZ" && document.getElementById('MZ_file').files[0]) {
        Upload_Files()
        setButtonText('Experiment Running') }
      if (level == "DM" && document.getElementById('MZ_file').files[0]) {
        Upload_Files()
        setButtonText('Experiment Running') }
      if (level == "AC" && document.getElementById('PP_file').files[0] &&
          document.getElementById('MD_file').files[0] && 
          document.getElementById('ACF_file').files[0] &&
          document.getElementById('TLF_file').files[0] &&
          document.getElementById('CBF_file').files[0] &&
          document.getElementById('FD_file').files[0] &&
          document.getElementById('IMS_file').files[0]) {
        Upload_Files()
        setButtonText('Experiment Running') }
      if (level == "STF" || level == "SIF" && document.getElementById('PP_file').files[0] &&
          document.getElementById('CBF_file').files[0] &&
          document.getElementById('ACF_file').files[0] &&
          document.getElementById('TLF_file').files[0] &&
          document.getElementById('IMS_file').files[0]) {
        Upload_Files()
        setButtonText('Experiment Running') }
      if (level == "SLIM" && document.getElementById('PP_file').files[0] &&
        document.getElementById('CBF_file').files[0] &&
        document.getElementById('ACF_file').files[0] &&
        document.getElementById('TLF_file').files[0] &&
        document.getElementById('MD_file').files[0]) {
        Upload_Files()
        setButtonText('Experiment Running') }
    }
  } 
  
//  Set state for input files
const inputFile = useState("empty")


// Handle all files.
// Send post request to API with parameters and files
const [data, setData] = useState();
const [isLoading, setIsLoading] = useState(false);
const [err, setErr] = useState('');
const Upload_Files = async () => {
  setIsLoading(true);
  try {
  var fileElement_pp = document.getElementById('PP_file').files[0];
      }
  catch (err) {
    setErr(err.message);
    }
  try {
  var fileElement_mz = document.getElementById('MZ_file').files[0];
      }
  catch (err) {
    setErr(err.message);
    }
  try {
    var fileElement_cbf = document.getElementById('CBF_file').files[0];
        }
  catch (err) {
    setErr(err.message);
      }
  try {
    var fileElement_acf = document.getElementById('ACF_file').files[0];
        }
  catch (err) {
    setErr(err.message);
      }
  try {
    var fileElement_tlf = document.getElementById('TLF_file').files[0];
        }
  catch (err) {
    setErr(err.message);
      }
  try {
    var fileElement_fd = document.getElementById('FD_file').files[0];
        }
  catch (err) {
    setErr(err.message);
      }
  try {
    var fileElement_ims = document.getElementById('IMS_file').files[0];
        }
  catch (err) {
    setErr(err.message);
      }
  try {
    var fileElement_md = document.getElementById('MD_file').files[0];
        }
  catch (err) {
    setErr(err.message);
      }
  var expname = document.getElementById('EXP_name').value;
  try {
    const {data} = await axios.post(
      'http://127.0.0.1:8000/api/',
      {ExperimentType: level, ExperimentName:expname ,PreprocessedDataFolder:fileElement_pp,
       mzMLDataFolder:fileElement_mz, FeatureDataFolder:fileElement_fd, CalibrantFile:fileElement_cbf,
       AutoCCSConfigFile:fileElement_acf,IMSMetadataFolder:fileElement_ims,
       TargetListFile:fileElement_tlf,MetadataFile:fileElement_md},
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Accept: 'application/json',
        },
      },
    );
    console.log(JSON.stringify(data, null, 4));
    setData(data);
  } catch (err) {
    setErr(err.message);
  } finally {
    setIsLoading(false);
  }
};


const [level, setLevel] = useStateWithCallback(0);
const changeLevel = (x) => {
  setLevel(x, (prevValue, newValue) => {
  console.log(newValue);})};

const [PP, setPP] = useStateWithCallback();
const AddPreProcessedData = (x) => {
  if (x == true) {
  setPP("PreProcessed Data", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setPP(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }

const [MZ, setMZ] = useStateWithCallback();
const AddMZData = (x) => {
  if (x == true) {
  setMZ("mzML Data", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setMZ(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }

const [CBF, setCBF] = useStateWithCallback();
const AddCalibrantFile = (x) => {
  if (x == true) {
  setCBF("Calibrant File", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setCBF(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }

const [ACF, setACF] = useStateWithCallback();
const AddAutoCCSConfigFile = (x) => {
  if (x == true) {
  setACF("AutoCCS Configuration File", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setACF(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }

const [TLF, setTLF] = useStateWithCallback();
const AddTargetListFile = (x) => {
  if (x == true) {
  setTLF("Target List File", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setTLF(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }

const [FD, setFD] = useStateWithCallback();
const AddFeatureDataFolder = (x) => {
  if (x == true) {
  setFD("Feature Data Folder", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setFD(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }

const [IMS, setIMS] = useStateWithCallback();
const AddIMSMetaDataFolder = (x) => {
  if (x == true) {
  setIMS("IMS Metadata Folder", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setIMS(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }

const [MD, setMD] = useStateWithCallback();
const AddMetadataFile = (x) => {
  if (x == true) {
    setMD("Metadata File", (prevValue, newValue) => {
  console.log(newValue);})}
  else  {
    setMD(null, (prevValue, newValue) => {
    console.log(newValue);})}
  ; }
// const [EXP, setEXP] = useStateWithCallback();
// const AddEXP = (x) => {
//   if (x == true) {
//     AddEXP("Experiment Name", (prevValue, newValue) => {
//   console.log(newValue);})}
//   else  {
//     setEXP(null, (prevValue, newValue) => {
//     console.log(newValue);})}
//   ; }



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
                <button level={1} disabled={level==="ST"} onClick={() => {changeLevel("ST");AddPreProcessedData(false);AddMZData(false);AddCalibrantFile(false);AddAutoCCSConfigFile(false);AddTargetListFile(false);AddFeatureDataFolder(false);AddIMSMetaDataFolder(false);AddMetadataFile(false);}}  className={level==="ST" || level==="PW" || level==="MZ" || level==="DM" || level==="AC" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>Single-Tool</button>
                <button level={1}  onClick={() => setLevel("PP")} disabled={true} className= {'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>PNNL PreProcessor</button>
              <div>
                </div>
                <button level={1} disabled={level==="SIF"} onClick={() => {changeLevel("SIF");AddPreProcessedData(true);AddMZData(false);AddCalibrantFile(true);AddAutoCCSConfigFile(true);AddTargetListFile(true);AddFeatureDataFolder(false);AddIMSMetaDataFolder(true);AddMetadataFile(false);}} className={level==="SIF" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>Single Field</button>
                <button level={1} disabled={level==="PW"} onClick={() => {changeLevel("PW");AddPreProcessedData(true);AddMZData(false);AddCalibrantFile(false);AddAutoCCSConfigFile(false);AddTargetListFile(false);AddFeatureDataFolder(false);AddIMSMetaDataFolder(false);AddMetadataFile(false);}} className={level==="PW" || level==="STF" || level==="SIF" || level==="SLIM"? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>Proteowizard</button>
              </div>
              <div>
                <button level={1} disabled={level==="STF"} onClick={() => {changeLevel("STF");AddPreProcessedData(true);AddMZData(false);AddCalibrantFile(true);AddAutoCCSConfigFile(true);AddTargetListFile(true);AddFeatureDataFolder(false);AddIMSMetaDataFolder(true);AddMetadataFile(false);}} className={level==="STF" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>Stepped Field</button>
                <button level={1}  disabled={level==="MZ"} onClick={() => {changeLevel("MZ");AddPreProcessedData(false);AddMZData(true);AddCalibrantFile(false);AddAutoCCSConfigFile(false);AddTargetListFile(false);AddFeatureDataFolder(false);AddIMSMetaDataFolder(false);AddMetadataFile(false);}}  className={level==="MZ" || level==="STF" || level==="SIF" || level==="SLIM"? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>Mzmine</button>
              </div>
              <div>
                <button level={1} disabled={level==="SLIM"} onClick={() => {changeLevel("SLIM");AddPreProcessedData(true);AddMZData(false);AddCalibrantFile(true);AddAutoCCSConfigFile(true);AddTargetListFile(true);AddFeatureDataFolder(false);AddIMSMetaDataFolder(false);AddMetadataFile(true);}}  className={level==="SLIM" ? 'btn--selected' : 'btn--not--selected'} buttonStyle='btn--outline' buttonSize='btn--large'>SLIM</button>
                <button level={1} onClick={() => {changeLevel("DM");AddPreProcessedData(false);AddMZData(true);AddCalibrantFile(false);AddAutoCCSConfigFile(false);AddTargetListFile(false);AddFeatureDataFolder(false);AddIMSMetaDataFolder(false);AddMetadataFile(false);}} disabled={level ===0 || level==="ST" || level==="MZ" || level==="AC" || level==="PW"  ? false: true} className={level==="DM" ? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>DEIMoS</button>
              </div>
              <div>
                <button level={1} disabled={false} className='btn--new' buttonStyle='btn--outline' buttonSize='btn--large'></button>
                <button  level={1} disabled={level==="AC"} onClick={() => {changeLevel("AC");AddPreProcessedData(true);AddMZData(false);AddCalibrantFile(true);AddAutoCCSConfigFile(true);AddTargetListFile(true);AddFeatureDataFolder(true);AddIMSMetaDataFolder(true);AddMetadataFile(true);}}  className={level==="AC" || level==="STF" || level==="SIF" || level==="SLIM"? 'btn--disabled--orange' : 'btn--new'} buttonStyle='btn--outline' buttonSize='btn--large'>AutoCCS</button>
              </div>
            </div>
            <div className="innest-container">
            <div style={{ fontSize: "1.5rem", "text-align": "center"}}>{level==0 || level == "ST" ? "Select a Tool or Workflow to Begin":"Upload Required Files Below" }</div>
            <form action="/test/data.html">
            {/* <fieldset>
            <legend>Upload Data</legend> */}
            <br></br>
            <br></br>
            <div><a style={{ fontSize: "1.4rem" }} >{PP}{' '}</a></div>
            {(PP != null) && <div><br></br></div>}
            <div><a style={{ fontSize: "1.4rem" }} >{MZ}{' '}</a></div>
            {(MZ != null) && <div><br></br></div>}
            <div><a style={{ fontSize: "1.4rem" }} >{CBF}{' '}</a></div>
            {(CBF != null) && <div><br></br></div>}
            <div><a style={{ fontSize: "1.4rem" }} >{ACF}{' '}</a></div>
            {(ACF != null) && <div><br></br></div>}
            <div><a style={{ fontSize: "1.4rem" }} >{TLF}{' '}</a></div>
            {(TLF != null) && <div><br></br></div>}
            <div><a style={{ fontSize: "1.4rem" }} >{FD}{' '}</a></div>
            {(FD != null) && <div><br></br></div>}
            <div><a style={{ fontSize: "1.4rem" }} >{IMS}{' '}</a></div>
            {(IMS != null) && <div><br></br></div>}
            <div><a style={{ fontSize: "1.4rem" }} >{MD}{' '}</a></div>
            {(MD != null) && <div><br></br></div>}
            {(level!='0' && level != 'ST') &&<div><a style={{ fontSize: "1.4rem" }} >{'Experiment Name'}</a></div>}
            {(level!='0' && level != 'ST') && <div><br></br></div>}
            </form>
            
          
            </div>
            <div className="innest-container_2">
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            
            {(PP != null) && <input style={{ fontSize: "1.2rem" }} type='file' id='PP_file'  ref={inputFile}/>}
            {(PP != null) && <div><br></br></div>}
            {(MZ != null) &&<input style={{ fontSize: "1.2rem" }} type='file' id='MZ_file' ref={inputFile}/>}
            {(MZ != null) && <div><br></br></div>}
            {(CBF != null) &&<input style={{ fontSize: "1.2rem" }} type='file' id='CBF_file' ref={inputFile}/>}
            {(CBF != null) && <div><br></br></div>}
            {(ACF != null) &&<input style={{ fontSize: "1.2rem" }} type='file' id='ACF_file' ref={inputFile}/>}
            {(ACF != null) && <div><br></br></div>}
            {(TLF != null) &&<input style={{ fontSize: "1.2rem" }} type='file' id='TLF_file' ref={inputFile}/>}
            {(TLF != null) && <div><br></br></div>}
            {(FD != null) &&<input style={{ fontSize: "1.2rem" }} type='file' id='FD_file' ref={inputFile}/>}
            {(FD != null) && <div><br></br></div>}
            {(IMS != null) &&<input style={{ fontSize: "1.2rem" }} type='file' id='IMS_file' ref={inputFile}/>}
            {(IMS != null) && <div><br></br></div>}
            {(MD != null) &&<input style={{ fontSize: "1.2rem" }} type='file' id='MD_file' ref={inputFile}/>}
            {(MD != null) && <div><br></br></div>}
            {(level!='0' && level != 'ST') &&<input style={{ fontSize: "1.2rem" }} type='text' id='EXP_name' ref={inputFile}/>}
            {/* {(MD != null) && <div><br></br></div>} */}


            </div>
            <div className="innest-container_3">
            {(level!="ST" && level!='0') && <button onClick={() => {handleClick()}} disabled={false} className='btn--new_2' buttonStyle='btn--outline' buttonSize='btn--large'>{buttonText}</button>}


              </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Experiment;