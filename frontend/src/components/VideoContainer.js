import React from 'react';
import './VideoContainer.css';

function VideoContainer({ videoRef, isLive, isLoading }) {
  return (
    <div className="video-container-wrapper">
      <div className={`video-container ${isLive ? 'live' : ''}`}>
        <video
          ref={videoRef}
          className="video-element"
          playsInline
          muted
        />
        {!isLive && (
          <div className="video-placeholder">
            <div className="placeholder-content">
              <span className="video-icon">📹</span>
              <p>Click "Start Live Video" to begin</p>
            </div>
          </div>
        )}
        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Processing...</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default VideoContainer;
