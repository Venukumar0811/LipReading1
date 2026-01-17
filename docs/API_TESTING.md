# API Testing Guide

## 1. Health Check

### Request
```bash
curl http://localhost:8000/health
```

### Response
```json
{
  "status": "healthy",
  "model": "CNN-LSTM Lip Reading Model",
  "version": "1.0.0"
}
```

---

## 2. Model Information

### Request
```bash
curl http://localhost:8000/api/model-info
```

### Response
```json
{
  "model_type": "CNN-LSTM",
  "input_shape": [96, 96, 3],
  "num_classes": 500,
  "vocabulary_size": 500,
  "device": "cpu"
}
```

---

## 3. Process Frame

### Request
```bash
curl -X POST http://localhost:8000/api/process-frame \
  -H "Content-Type: application/json" \
  -d '{
    "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRg...[base64 image data]..."
  }'
```

### Response
```json
{
  "text": "hello",
  "confidence": 0.87,
  "frame_info": {
    "width": 640,
    "height": 480,
    "channels": 3
  }
}
```

### Using Python Requests
```python
import requests
import base64
import cv2

# Read image
frame = cv2.imread('test_frame.jpg')
_, buffer = cv2.imencode('.jpg', frame)
base64_str = base64.b64encode(buffer).decode('utf-8')

# Make request
response = requests.post(
    'http://localhost:8000/api/process-frame',
    json={'frame': f'data:image/jpeg;base64,{base64_str}'}
)

result = response.json()
print(f"Prediction: {result['text']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

## 4. Reset Session

### Request
```bash
curl -X POST http://localhost:8000/api/reset
```

### Response
```json
{
  "status": "success",
  "message": "Frame history cleared"
}
```

---

## 5. API Documentation

### Swagger UI
Open browser to: http://localhost:8000/docs

### ReDoc
Open browser to: http://localhost:8000/redoc

---

## Testing with Postman

### 1. Import API

1. Go to **File** → **New** → **HTTP Request**
2. Set method to **POST**
3. URL: `http://localhost:8000/api/process-frame`
4. Headers: `Content-Type: application/json`

### 2. Create Test Data

```json
{
  "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

### 3. Run Collection

- Health Check: GET http://localhost:8000/health
- Process Frame: POST http://localhost:8000/api/process-frame
- Model Info: GET http://localhost:8000/api/model-info
- Reset: POST http://localhost:8000/api/reset

---

## Performance Testing

### Load Testing with Apache Bench

```bash
# Single request
ab -n 1 -c 1 http://localhost:8000/health

# 100 concurrent requests
ab -n 1000 -c 100 http://localhost:8000/health

# Measure response time
curl -w "@curl-format.txt" -o /dev/null http://localhost:8000/health
```

### Using Python

```python
import requests
import time
import statistics

times = []

for i in range(100):
    start = time.time()
    response = requests.get('http://localhost:8000/health')
    times.append((time.time() - start) * 1000)  # ms

print(f"Min: {min(times):.2f}ms")
print(f"Max: {max(times):.2f}ms")
print(f"Avg: {statistics.mean(times):.2f}ms")
print(f"Median: {statistics.median(times):.2f}ms")
```

---

## Frontend Integration Testing

### Test Frame Capture

```javascript
// Open console in Chrome DevTools

// Get video element
const video = document.querySelector('video');

// Capture frame
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
canvas.width = video.videoWidth;
canvas.height = video.videoHeight;
ctx.drawImage(video, 0, 0);

// Get base64
const imageData = canvas.toDataURL('image/jpeg', 0.8);

// Send to API
fetch('http://localhost:8000/api/process-frame', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ frame: imageData })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Debugging Tips

### Enable Verbose Logging

Backend:
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

Frontend:
```javascript
// In App.js
const DEBUG = true;
if (DEBUG) {
  console.log('Frame captured:', imageData.slice(0, 50));
  console.log('Response:', data);
}
```

### Check Network Requests

1. Open Chrome DevTools (F12)
2. Go to **Network** tab
3. Make a request
4. View request/response details

### Test with Real Video

```python
import cv2
import requests
import base64

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    _, buffer = cv2.imencode('.jpg', frame)
    base64_str = base64.b64encode(buffer).decode('utf-8')
    
    response = requests.post(
        'http://localhost:8000/api/process-frame',
        json={'frame': f'data:image/jpeg;base64,{base64_str}'},
        timeout=5
    )
    
    result = response.json()
    print(f"{result['text']} ({result['confidence']:.2%})")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Error Codes

| Code | Error | Solution |
|------|-------|----------|
| 400 | Invalid frame data | Ensure base64 encoding is correct |
| 404 | Not found | Check endpoint URL |
| 500 | Server error | Check backend logs |
| 503 | Service unavailable | Ensure backend is running |

---

## Expected Response Times

- Health Check: < 10ms
- Frame Processing: 80-150ms
- Model Inference: 50-100ms
- Network Latency: 20-50ms
- **Total**: ~120-250ms per frame

---

For more information, see [README.md](./README.md)
