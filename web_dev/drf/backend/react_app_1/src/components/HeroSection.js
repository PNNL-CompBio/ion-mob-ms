import React from 'react';
import { Button } from './Button';
import '../App.css';
import './HeroSection.css';



function HeroSection() {
  return (
    <div className='hero-container'>
        <video src={require('../videos/video-2.mp4')}
        autoPlay loop muted />
        <h1>Ion Mobility Dashboard</h1>
        <div className='hero-btns'>
            <Button className='btn' buttonStyle='btn--outline' buttonSize='btn--large'>
            Start Experiment
            </Button>
        </div>
        <div className='hero-btns'>
            <Button className='btn' buttonStyle='btn--primary' buttonSize='btn--medium'>
            View Tutorial Video <i className='far fa-play-circle' />
            </Button>
        </div>
    </div>
  )
}

export default HeroSection;