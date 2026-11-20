/**
 * Mobile App Global Configuration
 * 
 * Adjust API_BASE_URL to match your testing environment:
 * - Local iOS Simulator / Web: 'http://localhost:8000'
 * - Android Emulator: 'http://10.0.2.2:8000'
 * - Physical Device on Wi-Fi: 'http://<YOUR_LOCAL_IP>:8000' (e.g. 'http://192.168.1.150:8000')
 * - Vercel / Cloud URL: 'https://your-deployment.vercel.app'
 */

export const CONFIG = {
  // Supabase Authentication
  SUPABASE_URL: 'https://hlhkktramvskboiqnnju.supabase.co',
  SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsaGtrdHJhbXZza2JvaXFubmp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUxMTQxNDUsImV4cCI6MjExMDY5MDE0NX0.ec37e6bMKyLMhOsaIkzQhVZEm1KO5INbWxnt18Rv_9Q',

  // Backend API Endpoint (Live Vercel Production)
  API_BASE_URL: 'https://object-detection-suite.vercel.app',
  
  // Endpoint Paths
  HEALTH_PATH: '/api/health',
  DETECT_PATH: '/api/detect',

  // Default Inference Hyperparameters
  DEFAULT_CONF: 0.25,
  DEFAULT_IOU: 0.50,
  DEFAULT_IMGSZ: 640,

  // Network Timeout (milliseconds)
  TIMEOUT_MS: 45000,

  // App Metadata
  APP_NAME: 'VisionDetect Mobile',
  VERSION: '1.0.0',
};

export default CONFIG;
