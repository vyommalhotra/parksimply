import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const [currentFrame, setCurrentFrame] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => 
    {
      let str = '/get_display?timestamp=' + new Date().getTime().toString()
        fetch(str)
        .then(res => res.blob())
        .then(image =>
          {
            URL.revokeObjectURL(currentFrame);
            setCurrentFrame(URL.createObjectURL(image));
          }
        )         
    }, 500)
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Park Simply <br></br>
          Reading from /extractor/api/buffer.txt <br></br>
          {/* {currentFrame} */}
          <img src={currentFrame}/>
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
        </a>
      </header>
    </div>
  );
}

export default App;
