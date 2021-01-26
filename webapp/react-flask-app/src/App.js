import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const [currentFrame, setCurrentFrame] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {fetch('/get_car_ids').then(res => res.json()).then(data => {
      setCurrentFrame(data.data);
    }) }, 2000) 
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Park Simply <br></br>
          Reading from /extractor/api/buffer.txt <br></br>
          {currentFrame}
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
