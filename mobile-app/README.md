# VisionDetect Mobile App (React Native with Expo)

A cross-platform React Native mobile application powered by Expo and `expo-image-picker` for client-side image capture and real-time inference against the unified VisionDetect FastAPI backend.

---

## 🔒 Privacy & Architecture: Strict No-Storage Rule

This mobile application strictly enforces a **Zero-Storage Privacy Architecture**:
1. **Camera Roll Isolation**: Captured camera photos are processed via ephemeral cache URIs. They are never saved to the device's camera roll or persistent media library (`MediaLibrary.saveToLibraryAsync` is explicitly excluded).
2. **Ephemeral Memory Processing**: Images are streamed directly as multipart/form-data to the backend without persistent duplication.
3. **State & Cache Purging**: Pressing **Clear / Reset Memory** instantly resets `imageUri`, clears detected bounding boxes, and garbage-collects all local pointers.

---

## ⚙️ Configuration (`config.js`)

Edit `config.js` to point to your backend depending on how you run the app:

| Client Environment | `API_BASE_URL` in `config.js` |
| :--- | :--- |
| **Expo Web / iOS Simulator** | `http://localhost:8000` |
| **Android Emulator** | `http://10.0.2.2:8000` |
| **Physical Device (Expo Go via LAN)** | `http://<YOUR_COMPUTER_LOCAL_IP>:8000` (e.g. `http://192.168.1.150:8000`) |
| **Cloud Deployed Backend** | `https://your-domain.com` |

*Note: You can also tap the ⚙️ icon in the app header at any time to change the backend URL directly from your mobile device!*

---

## 🚀 Running the App

### 1. Install Dependencies
```bash
npm install
```

### 2. Start the Expo Development Server
```bash
npx expo start
```

### 3. Open on Your Platform of Choice
- Press `w` to open in your web browser (Expo Web)
- Press `a` to launch on a connected Android device / emulator
- Press `i` to launch on an iOS Simulator (macOS only)
- Scan the QR code using the **Expo Go** app on iOS or Android
