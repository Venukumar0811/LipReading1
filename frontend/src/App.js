import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import VideoContainer from './components/VideoContainer';
import ControlPanel from './components/ControlPanel';
import SubtitleBar from './components/SubtitleBar';
import ErrorMessage from './components/ErrorMessage';

function App() {
  const [isLive, setIsLive] = useState(false);
  const [subtitle, setSubtitle] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [history, setHistory] = useState([]);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const frameIntervalRef = useRef(null);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (frameIntervalRef.current) {
        clearInterval(frameIntervalRef.current);
      }
    };
  }, []);

  const startLiveVideo = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        },
        audio: false // Pure lip reading, no audio
      });

      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }

      setIsLive(true);
      setSubtitle('');
      startFrameCapture();
    } catch (err) {
      setError(
        err.name === 'NotAllowedError'
          ? 'Camera access denied. Please enable camera permissions.'
          : 'Failed to access camera. Ensure camera is available and working.'
      );
      console.error('Camera access error:', err);
    }
  };

  const stopLiveVideo = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (frameIntervalRef.current) {
      clearInterval(frameIntervalRef.current);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsLive(false);
    setSubtitle('');
  };

  const startFrameCapture = () => {
    // Capture frames every 500ms (approximately 2 FPS for processing)
    frameIntervalRef.current = setInterval(() => {
      captureAndProcessFrame();
    }, 500);
  };

  const captureAndProcessFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    try {
      const context = canvasRef.current.getContext('2d');
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      context.drawImage(videoRef.current, 0, 0);

      const imageData = canvasRef.current.toDataURL('image/jpeg', 0.8);

      setIsLoading(true);
      const response = await fetch(`${BACKEND_URL}/api/process-frame`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ frame: imageData })
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.statusText}`);
      }

      const data = await response.json();
      if (data.text) {
        setSubtitle(data.text);
        setConfidence(data.confidence || 0);

        // Add to history if it's a new prediction
        if (data.text && !history.includes(data.text)) {
          setHistory(prev => [data.text, ...prev].slice(0, 10));
        }
      }
    } catch (err) {
      console.error('Frame processing error:', err);
      // Don't show error for every frame, but log it
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎬 Lip Reading Application</h1>
        <p>Visual Speech Recognition Using Deep Learning</p>
      </header>

      <main className="app-main">
        <div className="content-wrapper">
          <VideoContainer
            videoRef={videoRef}
            isLive={isLive}
            isLoading={isLoading}
          />
          <SubtitleBar
            subtitle={subtitle}
            confidence={confidence}
            isLoading={isLoading}
          />
        </div>

        <ControlPanel
          isLive={isLive}
          onStart={startLiveVideo}
          onStop={stopLiveVideo}
          isLoading={isLoading}
        />

        {error && <ErrorMessage message={error} />}

        {/* Hidden canvas for frame capture */}
        <canvas ref={canvasRef} style={{ display: 'none' }} />

        {/* History Panel */}
        {history.length > 0 && (
          <div className="history-panel">
            <h3>Recent Predictions</h3>
            <ul>
              {history.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Final Year Project • Real-Time Lip Reading • CNN + LSTM Deep Learning Model</p>
      </footer>
    </div>
  );
}

export default App;
