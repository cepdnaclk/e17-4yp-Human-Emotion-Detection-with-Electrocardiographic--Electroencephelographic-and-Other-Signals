import React from 'react';
import { useRef } from "react";
import './App.css';

function App() {
  const videoRef = useRef(null);
  const onPlayButtonClickHandler = e => {
    videoRef.current.play()
    videoRef.current.requestFullscreen()
  }
  const onPauseButtonClickHandler = e => {
    videoRef.current.pause()
  }

  const onEndHandler = e => {
    videoRef.current.webkitExitFullscreen();
  }

  return (
    <React.Fragment>
      <h1 style={{ textAlign: 'center', margin: '10px 0px 0px 0px' }}>Video</h1>
      <div className='container-div'>
        <video width="480" height="300" controls ref={videoRef} onEnded={onEndHandler}>
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
