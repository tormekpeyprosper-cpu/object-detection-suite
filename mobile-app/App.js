import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  Image,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
  Dimensions,
  TextInput,
  Modal,
  SafeAreaView,
  StatusBar,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { StatusBar as ExpoStatusBar } from 'expo-status-bar';
import { createClient } from '@supabase/supabase-js';
import CONFIG from './config';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const PREVIEW_WIDTH = SCREEN_WIDTH - 32;

// Initialize Supabase Client for React Native
export const supabase = createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: false,
  },
});

// Vibrant neon color palette for bounding box overlays
const BOX_COLORS = ['#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#3b82f6'];

export default function App() {
  // Authentication State
  const [session, setSession] = useState(null);
  const [authMode, setAuthMode] = useState('signin'); // 'signin' or 'signup'
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState(null);
  const [authSuccess, setAuthSuccess] = useState(null);

  // Vision Detection State
  const [imageUri, setImageUri] = useState(null);
  const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0 });
  const [detections, setDetections] = useState([]);
  const [detectionLoading, setDetectionLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState({ connected: false, mode: 'unknown' });
  const [apiUrl, setApiUrl] = useState(CONFIG.API_BASE_URL);
  const [confThreshold, setConfThreshold] = useState(CONFIG.DEFAULT_CONF);
  const [settingsModalVisible, setSettingsModalVisible] = useState(false);
  const [inferenceMeta, setInferenceMeta] = useState(null);

  // Check Supabase session on startup
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  // Ping backend health
  useEffect(() => {
    checkBackendHealth();
  }, [apiUrl]);

  const checkBackendHealth = async () => {
    try {
      const cleanBase = apiUrl.replace(/\/api\/detect\/?$/, '');
      const response = await fetch(`${cleanBase}${CONFIG.HEALTH_PATH}`, { method: 'GET' });
      if (response.ok) {
        const data = await response.json();
        setBackendStatus({
          connected: true,
          mode: data.mode || 'mock',
        });
      } else {
        setBackendStatus({ connected: false, mode: 'offline' });
      }
    } catch (e) {
      setBackendStatus({ connected: false, mode: 'offline' });
    }
  };

  // ============================================================================
  // Authentication Handlers
  // ============================================================================
  const handleAuthSubmit = async () => {
    if (!authEmail.trim() || !authPassword) {
      setAuthError('Please enter both email and password.');
      return;
    }

    setAuthLoading(true);
    setAuthError(null);
    setAuthSuccess(null);

    try {
      if (authMode === 'signin') {
        const { data, error } = await supabase.auth.signInWithPassword({
          email: authEmail.trim(),
          password: authPassword,
        });
        if (error) throw error;
        setSession(data.session);
      } else {
        const { data, error } = await supabase.auth.signUp({
          email: authEmail.trim(),
          password: authPassword,
        });
        if (error) throw error;
        if (data.session) {
          setSession(data.session);
        } else {
          setAuthSuccess('Account created! Please check your email to confirm registration.');
        }
      }
    } catch (err) {
      setAuthError(err.message || 'Authentication failed.');
    } finally {
      setAuthLoading(false);
    }
  };

  const handleSignOut = async () => {
    try {
      await supabase.auth.signOut();
    } catch (err) {
      console.error('Sign out error:', err);
    } finally {
      setSession(null);
      handleClearAndReset();
    }
  };

  // ============================================================================
  // Vision Handlers (Strict Zero-Storage)
  // ============================================================================
  const handleTakePhoto = async () => {
    try {
      const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
      if (!permissionResult.granted) {
        Alert.alert('Permission Denied', 'Camera permission is required to capture images for detection.');
        return;
      }

      // STRICT ZERO-STORAGE: Ephemeral capture; never saved to camera roll
      const pickerResult = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 0.9,
        exif: false,
      });

      if (!pickerResult.canceled && pickerResult.assets && pickerResult.assets.length > 0) {
        const asset = pickerResult.assets[0];
        setImageUri(asset.uri);
        setImageDimensions({
          width: asset.width || 640,
          height: asset.height || 640,
        });
        setDetections([]);
        setInferenceMeta(null);

        await sendToDetectEndpoint(asset.uri, asset.width || 640, asset.height || 640);
      }
    } catch (error) {
      Alert.alert('Camera Error', error.message);
    }
  };

  const handlePickImage = async () => {
    try {
      const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!permissionResult.granted) {
        Alert.alert('Permission Denied', 'Media access permission is required to select photos.');
        return;
      }

      const pickerResult = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 0.9,
      });

      if (!pickerResult.canceled && pickerResult.assets && pickerResult.assets.length > 0) {
        const asset = pickerResult.assets[0];
        setImageUri(asset.uri);
        setImageDimensions({
          width: asset.width || 640,
          height: asset.height || 640,
        });
        setDetections([]);
        setInferenceMeta(null);

        await sendToDetectEndpoint(asset.uri, asset.width || 640, asset.height || 640);
      }
    } catch (error) {
      Alert.alert('Picker Error', error.message);
    }
  };

  const sendToDetectEndpoint = async (uri, originalW, originalH) => {
    if (!session || !session.access_token) {
      Alert.alert('Authentication Required', 'Please sign in to run object detection.');
      setSession(null);
      return;
    }

    setDetectionLoading(true);

    try {
      const cleanBase = apiUrl.replace(/\/api\/detect\/?$/, '');
      const targetEndpoint = `${cleanBase}${CONFIG.DETECT_PATH}`;

      const formData = new FormData();
      formData.append('file', {
        uri: uri,
        name: 'mobile_input.jpg',
        type: 'image/jpeg',
      });
      formData.append('conf', confThreshold.toString());
      formData.append('iou', CONFIG.DEFAULT_IOU.toString());
      formData.append('imgsz', CONFIG.DEFAULT_IMGSZ.toString());

      const response = await fetch(targetEndpoint, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (response.status === 401) {
        Alert.alert('Session Expired', 'Your authentication session has expired. Please sign in again.');
        handleSignOut();
        return;
      }

      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server returned status ${response.status}`);
      }

      const data = await response.json();
      setDetections(data.detections || []);
      setInferenceMeta({
        mode: data.mode,
        latency: data.inference_time_ms,
        count: data.detections_count,
        width: data.image?.width || originalW,
        height: data.image?.height || originalH,
      });
    } catch (err) {
      Alert.alert('Inference Failed', err.message);
    } finally {
      setDetectionLoading(false);
    }
  };

  const handleClearAndReset = () => {
    setImageUri(null);
    setImageDimensions({ width: 0, height: 0 });
    setDetections([]);
    setInferenceMeta(null);
  };

  const previewHeight = imageDimensions.width > 0
    ? (imageDimensions.height / imageDimensions.width) * PREVIEW_WIDTH
    : 240;

  // ============================================================================
  // RENDER VIEW: 1. If not authenticated -> Login / Sign-Up Screen
  // ============================================================================
  if (!session) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <ExpoStatusBar style="light" />
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.authContainer}
        >
          <ScrollView contentContainerStyle={styles.authScroll}>
            
            {/* Ambient Brand Header */}
            <View style={styles.authHeader}>
              <View style={styles.authBrandBadge}>
                <Text style={styles.authBrandBadgeText}>V</Text>
              </View>
              <Text style={styles.authTitle}>VisionDetect AI</Text>
              <Text style={styles.authSubtitle}>Zero-Storage In-Memory Vision</Text>
            </View>

            {/* Auth Glass Card */}
            <View style={styles.authCard}>
              
              {/* Tab Switcher */}
              <View style={styles.authTabs}>
                <TouchableOpacity
                  style={[styles.authTabBtn, authMode === 'signin' && styles.authTabBtnActive]}
                  onPress={() => {
                    setAuthMode('signin');
                    setAuthError(null);
                    setAuthSuccess(null);
                  }}
                >
                  <Text style={[styles.authTabText, authMode === 'signin' && styles.authTabTextActive]}>
                    Sign In
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.authTabBtn, authMode === 'signup' && styles.authTabBtnActive]}
                  onPress={() => {
                    setAuthMode('signup');
                    setAuthError(null);
                    setAuthSuccess(null);
                  }}
                >
                  <Text style={[styles.authTabText, authMode === 'signup' && styles.authTabTextActive]}>
                    Create Account
                  </Text>
                </TouchableOpacity>
              </View>

              {/* Feedback Alerts */}
              {authError && (
                <View style={styles.authAlertError}>
                  <Text style={styles.authAlertErrorText}>{authError}</Text>
                </View>
              )}
              {authSuccess && (
                <View style={styles.authAlertSuccess}>
                  <Text style={styles.authAlertSuccessText}>{authSuccess}</Text>
                </View>
              )}

              {/* Email Field */}
              <Text style={styles.inputLabel}>Email Address</Text>
              <TextInput
                style={styles.textInput}
                value={authEmail}
                onChangeText={setAuthEmail}
                placeholder="name@example.com"
                placeholderTextColor="#64748b"
                autoCapitalize="none"
                keyboardType="email-address"
                autoCorrect={false}
              />

              {/* Password Field */}
              <Text style={[styles.inputLabel, { marginTop: 12 }]}>Password</Text>
              <View style={styles.passwordRow}>
                <TextInput
                  style={[styles.textInput, { flex: 1 }]}
                  value={authPassword}
                  onChangeText={setAuthPassword}
                  placeholder="••••••••"
                  placeholderTextColor="#64748b"
                  secureTextEntry={!showPassword}
                  autoCapitalize="none"
                />
                <TouchableOpacity
                  style={styles.pwdToggleBtn}
                  onPress={() => setShowPassword(!showPassword)}
                >
                  <Text style={styles.pwdToggleText}>{showPassword ? '🔒' : '👁️'}</Text>
                </TouchableOpacity>
              </View>

              {/* Submit Button */}
              <TouchableOpacity
                style={styles.authSubmitBtn}
                onPress={handleAuthSubmit}
                disabled={authLoading}
              >
                {authLoading ? (
                  <ActivityIndicator color="#fff" size="small" />
                ) : (
                  <Text style={styles.authSubmitText}>
                    {authMode === 'signin' ? 'Sign In' : 'Create Account'}
                  </Text>
                )}
              </TouchableOpacity>

              <Text style={styles.authPrivacyNote}>
                🔒 <Text style={{ fontWeight: 'bold' }}>Strict Zero-Storage:</Text> Analyzed in volatile memory only. Photos are never saved to disk, PostgreSQL, or Supabase Storage.
              </Text>

            </View>

          </ScrollView>
        </KeyboardAvoidingView>
      </SafeAreaView>
    );
  }

  // ============================================================================
  // RENDER VIEW: 2. Authenticated Detection Studio
  // ============================================================================
  return (
    <SafeAreaView style={styles.safeArea}>
      <ExpoStatusBar style="light" />
      
      {/* App Header */}
      <View style={styles.header}>
        <View style={styles.brandRow}>
          <View style={styles.brandBadge}>
            <Text style={styles.brandBadgeText}>V</Text>
          </View>
          <View>
            <Text style={styles.headerTitle}>VisionDetect AI</Text>
            <Text style={styles.headerSubtitle} numberOfLines={1}>
              {session.user.email}
            </Text>
          </View>
        </View>

        <View style={styles.headerActions}>
          <TouchableOpacity
            style={styles.settingsIconBtn}
            onPress={() => setSettingsModalVisible(true)}
          >
            <Text style={styles.settingsIconText}>⚙️</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.signOutBtn} onPress={handleSignOut}>
            <Text style={styles.signOutText}>Sign Out</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Backend Status Bar */}
      <View style={styles.statusBar}>
        <View
          style={[
            styles.statusDot,
            backendStatus.connected
              ? backendStatus.mode === 'ultralytics'
                ? styles.dotConnected
                : styles.dotMock
              : styles.dotOffline,
          ]}
        />
        <Text style={styles.statusLabel}>
          {backendStatus.connected
            ? `Backend: ${backendStatus.mode.toUpperCase()} MODE`
            : 'Backend: OFFLINE (Check Host / IP)'}
        </Text>
        <TouchableOpacity onPress={checkBackendHealth} style={styles.statusRefreshBtn}>
          <Text style={styles.statusRefreshText}>Ping</Text>
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        {/* Strict No-Storage Privacy Banner */}
        <View style={styles.privacyBanner}>
          <Text style={styles.privacyBannerTitle}>🔒 STRICT ZERO-STORAGE POLICY</Text>
          <Text style={styles.privacyBannerText}>
            Frames are processed strictly in-memory. Zero images are saved to your camera roll, disk, or remote databases.
          </Text>
        </View>

        {/* Image Preview & Bounding Box Overlay Viewport */}
        <View style={styles.viewport}>
          {imageUri ? (
            <View style={[styles.imageContainer, { width: PREVIEW_WIDTH, height: previewHeight }]}>
              <Image
                source={{ uri: imageUri }}
                style={[styles.previewImage, { width: PREVIEW_WIDTH, height: previewHeight }]}
                resizeMode="contain"
              />

              {/* Render Responsive Bounding Boxes */}
              {detections.map((det, idx) => {
                const color = BOX_COLORS[idx % BOX_COLORS.length];
                let left = 0, top = 0, width = 0, height = 0;

                if (det.relative_box) {
                  left = det.relative_box.x_min * PREVIEW_WIDTH;
                  top = det.relative_box.y_min * previewHeight;
                  width = (det.relative_box.x_max - det.relative_box.x_min) * PREVIEW_WIDTH;
                  height = (det.relative_box.y_max - det.relative_box.y_min) * previewHeight;
                } else if (imageDimensions.width > 0 && imageDimensions.height > 0) {
                  const scaleX = PREVIEW_WIDTH / imageDimensions.width;
                  const scaleY = previewHeight / imageDimensions.height;
                  left = det.box.x1 * scaleX;
                  top = det.box.y1 * scaleY;
                  width = (det.box.x2 - det.box.x1) * scaleX;
                  height = (det.box.y2 - det.box.y1) * scaleY;
                }

                const confPct = Math.round(det.confidence * 100);

                return (
                  <View
                    key={`det-${idx}`}
                    style={[
                      styles.boundingBox,
                      {
                        left: Math.max(0, left),
                        top: Math.max(0, top),
                        width: Math.max(10, width),
                        height: Math.max(10, height),
                        borderColor: color,
                        backgroundColor: `${color}22`,
                      },
                    ]}
                  >
                    <View style={[styles.boxLabelBadge, { backgroundColor: color }]}>
                      <Text style={styles.boxLabelText}>
                        {det.name} {confPct}%
                      </Text>
                    </View>
                  </View>
                );
              })}
            </View>
          ) : (
            <View style={styles.emptyPlaceholder}>
              <Text style={styles.emptyIcon}>📷</Text>
              <Text style={styles.emptyTitle}>No Image Selected</Text>
              <Text style={styles.emptySubtitle}>
                Take a photo or pick an image to perform zero-storage detection.
              </Text>
            </View>
          )}

          {/* Loading Overlay */}
          {detectionLoading && (
            <View style={styles.loadingOverlay}>
              <ActivityIndicator size="large" color="#06b6d4" />
              <Text style={styles.loadingText}>Running Vision Detection...</Text>
            </View>
          )}
        </View>

        {/* Action Buttons */}
        <View style={styles.actionsContainer}>
          <TouchableOpacity
            style={[styles.btn, styles.btnCamera]}
            onPress={handleTakePhoto}
            disabled={detectionLoading}
          >
            <Text style={styles.btnIcon}>📸</Text>
            <Text style={styles.btnText}>Take Photo</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.btn, styles.btnGallery]}
            onPress={handlePickImage}
            disabled={detectionLoading}
          >
            <Text style={styles.btnIcon}>🖼️</Text>
            <Text style={styles.btnText}>Pick Image</Text>
          </TouchableOpacity>
        </View>

        {imageUri && (
          <TouchableOpacity
            style={[styles.btn, styles.btnReset]}
            onPress={handleClearAndReset}
            disabled={detectionLoading}
          >
            <Text style={styles.btnResetText}>🗑️ Clear / Reset Memory</Text>
          </TouchableOpacity>
        )}

        {/* Detections Summary & Metadata */}
        {inferenceMeta && (
          <View style={styles.resultsCard}>
            <Text style={styles.resultsHeader}>Detection Results</Text>
            
            <View style={styles.metaRow}>
              <View style={styles.metaBadge}>
                <Text style={styles.metaBadgeLabel}>MODE</Text>
                <Text style={styles.metaBadgeVal}>{inferenceMeta.mode.toUpperCase()}</Text>
              </View>
              <View style={styles.metaBadge}>
                <Text style={styles.metaBadgeLabel}>LATENCY</Text>
                <Text style={styles.metaBadgeVal}>{inferenceMeta.latency} ms</Text>
              </View>
              <View style={styles.metaBadge}>
                <Text style={styles.metaBadgeLabel}>COUNT</Text>
                <Text style={styles.metaBadgeVal}>{inferenceMeta.count}</Text>
              </View>
            </View>

            {detections.length === 0 ? (
              <Text style={styles.noDetectionsText}>
                No objects met the {confThreshold} confidence threshold.
              </Text>
            ) : (
              detections.map((item, i) => (
                <View key={`item-${i}`} style={styles.detectionRow}>
                  <View style={styles.detectionLeft}>
                    <View style={[styles.rowColorDot, { backgroundColor: BOX_COLORS[i % BOX_COLORS.length] }]} />
                    <Text style={styles.detectionName}>{item.name}</Text>
                  </View>
                  <View style={styles.detectionRight}>
                    <Text style={styles.confidenceScore}>
                      {Math.round(item.confidence * 100)}%
                    </Text>
                  </View>
                </View>
              ))
            )}
          </View>
        )}

      </ScrollView>

      {/* Settings Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={settingsModalVisible}
        onRequestClose={() => setSettingsModalVisible(false)}
      >
        <View style={styles.modalBackdrop}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalTitle}>Network & Inference Settings</Text>

            <Text style={styles.inputLabel}>Backend Base URL</Text>
            <TextInput
              style={styles.textInput}
              value={apiUrl}
              onChangeText={setApiUrl}
              placeholder="http://192.168.1.X:8000"
              placeholderTextColor="#64748b"
              autoCapitalize="none"
              autoCorrect={false}
            />
            <Text style={styles.helperText}>
              • iOS Simulator / Web: http://localhost:8000{'\n'}
              • Android Emulator: http://10.0.2.2:8000{'\n'}
              • Physical Device: http://{'<YOUR_LAN_IP>'}:8000{'\n'}
              • Vercel Deployment: https://your-project.vercel.app
            </Text>

            <Text style={[styles.inputLabel, { marginTop: 14 }]}>
              Confidence Threshold ({confThreshold})
            </Text>
            <View style={styles.confSelectorRow}>
              {[0.15, 0.25, 0.40, 0.60].map((val) => (
                <TouchableOpacity
                  key={val}
                  style={[
                    styles.confOption,
                    confThreshold === val && styles.confOptionActive,
                  ]}
                  onPress={() => setConfThreshold(val)}
                >
                  <Text
                    style={[
                      styles.confOptionText,
                      confThreshold === val && styles.confOptionTextActive,
                    ]}
                  >
                    {val}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            <TouchableOpacity
              style={styles.modalCloseBtn}
              onPress={() => {
                setSettingsModalVisible(false);
                checkBackendHealth();
              }}
            >
              <Text style={styles.modalCloseText}>Save & Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0f172a',
    paddingTop: StatusBar.currentHeight || 0,
  },
  // Auth Screen Styles (Cyberpunk Dark Glassmorphism)
  authContainer: {
    flex: 1,
  },
  authScroll: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  authHeader: {
    alignItems: 'center',
    marginBottom: 24,
  },
  authBrandBadge: {
    width: 56,
    height: 56,
    borderRadius: 14,
    backgroundColor: '#06b6d4',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
    shadowColor: '#06b6d4',
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 8,
  },
  authBrandBadgeText: {
    color: '#ffffff',
    fontSize: 26,
    fontWeight: 'bold',
  },
  authTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#f8fafc',
    marginBottom: 4,
  },
  authSubtitle: {
    fontSize: 12,
    color: '#94a3b8',
  },
  authCard: {
    backgroundColor: 'rgba(30, 41, 59, 0.85)',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.4,
    shadowRadius: 16,
    elevation: 10,
  },
  authTabs: {
    flexDirection: 'row',
    backgroundColor: '#0f172a',
    borderRadius: 8,
    padding: 3,
    marginBottom: 16,
  },
  authTabBtn: {
    flex: 1,
    paddingVertical: 8,
    alignItems: 'center',
    borderRadius: 6,
  },
  authTabBtnActive: {
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: 'rgba(6, 182, 212, 0.4)',
  },
  authTabText: {
    color: '#94a3b8',
    fontWeight: '600',
    fontSize: 12,
  },
  authTabTextActive: {
    color: '#06b6d4',
  },
  authAlertError: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(239, 68, 68, 0.4)',
    borderRadius: 6,
    padding: 10,
    marginBottom: 12,
  },
  authAlertErrorText: {
    color: '#fca5a5',
    fontSize: 12,
  },
  authAlertSuccess: {
    backgroundColor: 'rgba(16, 185, 129, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.4)',
    borderRadius: 6,
    padding: 10,
    marginBottom: 12,
  },
  authAlertSuccessText: {
    color: '#6ee7b7',
    fontSize: 12,
  },
  passwordRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  pwdToggleBtn: {
    position: 'absolute',
    right: 12,
    padding: 4,
  },
  pwdToggleText: {
    fontSize: 16,
  },
  authSubmitBtn: {
    backgroundColor: '#06b6d4',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 18,
    shadowColor: '#06b6d4',
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  authSubmitText: {
    color: '#0f172a',
    fontWeight: 'bold',
    fontSize: 14,
  },
  authPrivacyNote: {
    marginTop: 16,
    fontSize: 10,
    color: '#64748b',
    textAlign: 'center',
    lineHeight: 14,
  },

  // Studio Header
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
    backgroundColor: '#0f172a',
  },
  brandRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  brandBadge: {
    width: 32,
    height: 32,
    borderRadius: 8,
    backgroundColor: '#06b6d4',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  brandBadgeText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
  },
  headerTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#f8fafc',
  },
  headerSubtitle: {
    fontSize: 11,
    color: '#06b6d4',
    maxWidth: 160,
  },
  headerActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  settingsIconBtn: {
    padding: 6,
  },
  settingsIconText: {
    fontSize: 18,
  },
  signOutBtn: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(239, 68, 68, 0.4)',
    paddingHorizontal: 8,
    paddingVertical: 5,
    borderRadius: 6,
  },
  signOutText: {
    color: '#f87171',
    fontSize: 11,
    fontWeight: '600',
  },
  statusBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1e293b',
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  dotConnected: {
    backgroundColor: '#10b981',
  },
  dotMock: {
    backgroundColor: '#f59e0b',
  },
  dotOffline: {
    backgroundColor: '#ef4444',
  },
  statusLabel: {
    flex: 1,
    fontSize: 11,
    color: '#cbd5e1',
    fontWeight: '500',
  },
  statusRefreshBtn: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    backgroundColor: '#334155',
  },
  statusRefreshText: {
    fontSize: 10,
    color: '#06b6d4',
    fontWeight: '600',
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  privacyBanner: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    borderColor: 'rgba(16, 185, 129, 0.3)',
    borderWidth: 1,
    borderRadius: 8,
    padding: 10,
    marginBottom: 16,
  },
  privacyBannerTitle: {
    color: '#10b981',
    fontWeight: '700',
    fontSize: 11,
    marginBottom: 2,
  },
  privacyBannerText: {
    color: '#a7f3d0',
    fontSize: 11,
    lineHeight: 15,
  },
  viewport: {
    width: PREVIEW_WIDTH,
    minHeight: 240,
    backgroundColor: '#1e293b',
    borderRadius: 12,
    overflow: 'hidden',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
    position: 'relative',
    marginBottom: 16,
  },
  imageContainer: {
    position: 'relative',
    justifyContent: 'center',
    alignItems: 'center',
  },
  previewImage: {
    borderRadius: 8,
  },
  emptyPlaceholder: {
    alignItems: 'center',
    padding: 24,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 8,
  },
  emptyTitle: {
    color: '#f8fafc',
    fontSize: 15,
    fontWeight: '600',
    marginBottom: 4,
  },
  emptySubtitle: {
    color: '#64748b',
    fontSize: 12,
    textAlign: 'center',
    maxWidth: 240,
  },
  loadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(15, 23, 42, 0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#f8fafc',
    marginTop: 10,
    fontSize: 13,
    fontWeight: '600',
  },
  boundingBox: {
    position: 'absolute',
    borderWidth: 2,
    borderRadius: 4,
  },
  boxLabelBadge: {
    position: 'absolute',
    top: -20,
    left: 0,
    paddingHorizontal: 4,
    paddingVertical: 2,
    borderRadius: 4,
  },
  boxLabelText: {
    color: '#ffffff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  actionsContainer: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 12,
  },
  btn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 10,
  },
  btnCamera: {
    backgroundColor: '#0284c7',
  },
  btnGallery: {
    backgroundColor: '#334155',
  },
  btnIcon: {
    fontSize: 18,
    marginRight: 6,
  },
  btnText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
  btnReset: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(239, 68, 68, 0.4)',
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 16,
  },
  btnResetText: {
    color: '#f87171',
    fontWeight: '600',
    fontSize: 13,
  },
  resultsCard: {
    backgroundColor: '#1e293b',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  resultsHeader: {
    color: '#f8fafc',
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 12,
  },
  metaRow: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 14,
  },
  metaBadge: {
    flex: 1,
    backgroundColor: '#0f172a',
    borderRadius: 6,
    padding: 8,
    alignItems: 'center',
  },
  metaBadgeLabel: {
    color: '#64748b',
    fontSize: 9,
    fontWeight: '700',
  },
  metaBadgeVal: {
    color: '#06b6d4',
    fontSize: 13,
    fontWeight: '700',
    marginTop: 2,
  },
  noDetectionsText: {
    color: '#94a3b8',
    fontSize: 12,
    textAlign: 'center',
    marginVertical: 8,
  },
  detectionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  detectionLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rowColorDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: 8,
  },
  detectionName: {
    color: '#f8fafc',
    fontSize: 13,
    fontWeight: '500',
  },
  detectionRight: {
    backgroundColor: '#0f172a',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
  },
  confidenceScore: {
    color: '#10b981',
    fontWeight: '700',
    fontSize: 12,
  },
  modalBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'center',
    padding: 20,
  },
  modalContainer: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: '#334155',
  },
  modalTitle: {
    color: '#f8fafc',
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 16,
  },
  inputLabel: {
    color: '#94a3b8',
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 6,
  },
  textInput: {
    backgroundColor: '#0f172a',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
    color: '#f8fafc',
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 13,
  },
  helperText: {
    color: '#64748b',
    fontSize: 11,
    marginTop: 6,
    lineHeight: 16,
  },
  confSelectorRow: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 6,
  },
  confOption: {
    flex: 1,
    paddingVertical: 8,
    borderRadius: 6,
    backgroundColor: '#0f172a',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
  },
  confOptionActive: {
    backgroundColor: '#0284c7',
    borderColor: '#0284c7',
  },
  confOptionText: {
    color: '#94a3b8',
    fontWeight: '600',
    fontSize: 12,
  },
  confOptionTextActive: {
    color: '#ffffff',
  },
  modalCloseBtn: {
    marginTop: 20,
    backgroundColor: '#06b6d4',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  modalCloseText: {
    color: '#0f172a',
    fontWeight: 'bold',
    fontSize: 14,
  },
});
