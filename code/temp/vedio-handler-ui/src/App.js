import React from 'react';
import { useRef } from "react";
import './App.css';

function App() {
  const vedioRef = useRef(null);
  const onPlayButtonClickHandler = e => {
    vedioRef.current.play()
  }
  const onPauseButtonClickHandler = e => {
    vedioRef.current.pause()
  }
  return (
    <React.Fragment>
      <h1 style={{textAlign: 'center', margin: '10px 0px 0px 0px'}}>Vedio</h1>
      <div className='container-div'>
        <video width="480" height="300" controls ref={vedioRef}>
          <source src="/vedios/mov_bbb.mp4" type="video/mp4" />
          Sorry, your browser doesn't support videos.
        </video>
      </div>
      <div className='container-div'>
        <button onClick={onPlayButtonClickHandler} className='button'>Play</button>
        <button onClick={onPauseButtonClickHandler} className='button'>Pause</button>
      </div>
    </React.Fragment>
  );
}

export default App;
