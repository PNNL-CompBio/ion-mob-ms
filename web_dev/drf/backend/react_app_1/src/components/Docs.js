import React from 'react';
import { Button } from './Button';
import '../App.css';
import './Docs.css';



function Documentation() {
  return (
    <>
    <div className='doc-header'>
        <h1>Documentation</h1>
    </div>
        <div className='doc-container'>
            <div className='doc-title'>Ion Mobility Dashboard</div>
            <div className='doc-description'>The Ion Mobility Dashboard is designed to allow scientists to generate results from raw Ion Mobility-Mass Spectrometry data without requiring assistance from an engineer or bioinformatician. This dashboard links four sequential command line docs into a single user-friendly application which communicates with Docker Desktop to dynamically spin up docker containers and manage the filesystem. Each doc has been dockerized and together they perform the following steps: quality control data processing, file type conversion (from proprietary to an open-source format), detection of unique features, and calculation of collision-cross section (CCS).</div>
        </div>
        <div className='doc-container'>
            <div className='doc-title'>IMS-MS Background</div>
            <div className='doc-description'>Mass Spectrometry (MS) is used to identify and differentiate unknown molecules by comparing intensities and mass-to-charge-ratio (m/z). This is important in clinical research and drug development, however, this method stuggles with identifying small molecules, isomers, and enantiomers. To increase the accuracy of molecular identification, MS can be paired with Ion Mobility Spectrometry (IMS). IMS generates an additional descriptive variable called the “collision cross section”, or CCS, which is used to further differentiate between unknown molecules.</div>
        </div>
        <div className='doc-container'>
            <div className='doc-subtitle'>Drift Tube Ion Mobility Spectrometry</div>
            <div className='doc-description'>Drift Tube Ion Mobility Spectrometry (DTIMS) seperates ions by collision cross section. This works by accelerating ions through a straight tube filled with an inert buffer gas, as the ions pass through the tube, they bump into buffer gas molecules and are slowed down. Drift (retention) time is used as a predictor of CCS. Ions with a greater CCS collide with and are slowed down more by buffer molecules, the inverse is true with small molecules. Single field DTIMS uses a single electrical field to accelerate ions through the tube. This differs from stepped field DTIMS which uses an alternating electrical curent to propel ions though the tube. An increase in the length of drift tube increases resolution and both methods of DTIMS are limited by instrument space.</div>
        </div>
        <div className='doc-container'>
            <div className='doc-subtitle'>Structures for Lossless Ion Manipulations</div>
            <div className='doc-description'>SLIM uses the same principal as single field DTIMS without the limitation of drift tube length. This technology allows the ions to be pushed around corners without colliding with path walls; this allows for significantly longer paths resulting in much greater resolution of ion CCS values.</div>
        </div>
        <div className='doc-container'>
            <div className='doc-title'>Instructions</div>
            <div className='doc-description'>Instructions on usage goes here... update later in the project</div>
        </div>
        

        </>      
  );
}

export default Documentation;