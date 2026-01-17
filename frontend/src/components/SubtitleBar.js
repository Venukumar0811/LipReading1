import React from 'react';
import './SubtitleBar.css';

function SubtitleBar({ subtitle, confidence, isLoading }) {
  const confidencePercent = Math.round(confidence * 100);

  return (
    <div className="subtitle-bar-wrapper">
      <div className={`subtitle-bar ${isLoading ? 'loading' : ''}`}>
        <div className="subtitle-content">
          <p className="subtitle-text">
            {subtitle || (isLoading ? 'Listening...' : 'Ready')}
          </p>
          {confidence > 0 && (
            <div className="confidence-display">
              <span className="confidence-label">Confidence:</span>
              <div className="confidence-bar">
                <div
                  className="confidence-fill"
                  style={{
                    width: `${confidencePercent}%`,
                    backgroundColor: confidencePercent > 70 ? '#00d9ff' : 
                                     confidencePercent > 40 ? '#ffb800' : '#ff6b6b'
                  }}
                ></div>
              </div>
              <span className="confidence-percent">{confidencePercent}%</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SubtitleBar;
