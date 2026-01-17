import React, { useEffect, useState } from 'react';
import './ErrorMessage.css';

function ErrorMessage({ message }) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(false), 6000);
    return () => clearTimeout(timer);
  }, [message]);

  if (!isVisible) return null;

  return (
    <div className="error-message">
      <span className="error-icon">⚠️</span>
      <span className="error-text">{message}</span>
      <button
        className="error-close"
        onClick={() => setIsVisible(false)}
      >
        ✕
      </button>
    </div>
  );
}

export default ErrorMessage;
