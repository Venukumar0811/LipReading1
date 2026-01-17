import React from 'react';
import './ControlPanel.css';

function ControlPanel({ isLive, onStart, onStop, isLoading }) {
  return (
    <div className="control-panel">
      <div className="button-group">
        <button
          className={`btn btn-primary ${isLive ? 'active' : ''}`}
          onClick={onStart}
          disabled={isLive || isLoading}
        >
          <span className="btn-icon">▶️</span>
          Start Live Video
        </button>

        <button
          className={`btn btn-danger ${isLive ? 'active' : ''}`}
          onClick={onStop}
          disabled={!isLive}
        >
          <span className="btn-icon">⏹️</span>
          Stop Video
        </button>
      </div>

      <div className="status-info">
        <div className={`status-badge ${isLive ? 'live' : 'inactive'}`}>
          <span className="status-dot"></span>
          {isLive ? 'LIVE' : 'INACTIVE'}
        </div>
      </div>
    </div>
  );
}

export default ControlPanel;
