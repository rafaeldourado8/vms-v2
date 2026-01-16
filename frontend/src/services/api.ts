import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/store/authStore'
import type {
  AuthResponse,
  Camera,
  CameraCreateRequest,
  Clip,
  ClipCreateRequest,
  DashboardStats,
  Detection,
  LoginRequest,
  Mosaico,
  MosaicoCreateRequest,
  PaginatedResponse,
  User,
} from '@/types'

// Criar instância do Axios
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().accessToken
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para refresh token
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const refreshToken = useAuthStore.getState().refreshToken
      if (refreshToken) {
        try {
          const { data } = await axios.post<{ access: string }>('/api/auth/refresh/', {
            refresh: refreshToken,
          })
          
          useAuthStore.getState().updateTokens(data.access)
          originalRequest.headers.Authorization = `Bearer ${data.access}`
          
          return api(originalRequest)
        } catch {
          useAuthStore.getState().logout()
          window.location.href = '/login'
        }
      }
    }
    
    return Promise.reject(error)
  }
)

// ======================================================
// AUTH
// ======================================================

export const authService = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const { data } = await api.post<AuthResponse>('/auth/login/', credentials)
    return data
  },

  async logout(refreshToken: string): Promise<void> {
    await api.post('/auth/logout/', { refresh_token: refreshToken })
  },

  async getMe(): Promise<User> {
    const { data } = await api.get<User>('/auth/me/')
    return data
  },
}

// ======================================================
// CAMERAS
// ======================================================

export const cameraService = {
  async list(): Promise<Camera[]> {
    const { data } = await api.get<Camera[] | PaginatedResponse<Camera>>('/cameras/')
    return Array.isArray(data) ? data : data.results
  },

  async get(id: number): Promise<Camera> {
    const { data } = await api.get<Camera>(`/cameras/${id}/`)
    return data
  },

  async create(camera: CameraCreateRequest): Promise<Camera> {
    const { data } = await api.post<Camera>('/cameras/', camera)
    return data
  },

  async update(id: number, camera: Partial<CameraCreateRequest>): Promise<Camera> {
    const { data } = await api.patch<Camera>(`/cameras/${id}/`, camera)
    return data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/cameras/${id}/`)
  },

  async updateDetectionConfig(id: number, config: {
    roi_areas: any[]
    virtual_lines: any[]
    tripwires: any[]
    zone_triggers: any[]
    recording_retention_days?: number
    ai_enabled?: boolean
  }): Promise<void> {
    await api.post(`/cameras/${id}/update_detection_config/`, config)
  },

  async toggleAI(id: number, enabled: boolean): Promise<void> {
    await api.post(`/cameras/${id}/toggle_ai/`, { enabled })
  },

  async getStream(id: number): Promise<{ stream_url: string; camera_id: number; current_streams: number; max_streams: number }> {
    const { data } = await api.get(`/cameras/${id}/stream/`)
    return data
  },
}

// ======================================================
// DETECTION (LPR Events)
// ======================================================

export const detectionService = {
  async listLprEvents(params?: {
    camera_id?: string
    plate?: string
    limit?: number
  }) {
    const { data } = await api.get('http://localhost:8002/api/events/lpr', { params })
    return data
  },

  async getLprEvent(eventId: string) {
    const { data } = await api.get(`http://localhost:8002/api/events/lpr/${eventId}`)
    return data
  },

  async listObjectEvents(params?: {
    camera_id?: string
    object_type?: string
    limit?: number
  }) {
    const { data } = await api.get('http://localhost:8002/api/events/objects', { params })
    return data
  },
}

// ======================================================
// DASHBOARD
// ======================================================

export const dashboardService = {
  async getStats(): Promise<DashboardStats> {
    const { data } = await api.get<DashboardStats>('/dashboard/stats/')
    return data
  },
}

// ======================================================
// STREAMING
// ======================================================

export const streamingService = {
  async startStream(cameraId: string, rtspUrl: string) {
    const { data } = await api.post('/streams/start', {
      camera_id: cameraId,
      source_url: rtspUrl,
    })
    return data
  },

  async stopStream(streamId: string) {
    await api.post(`/streams/${streamId}/stop`)
  },

  async getStream(streamId: string) {
    const { data } = await api.get(`/streams/${streamId}`)
    return data
  },

  async startRecording(streamId: string, retentionDays: number = 7) {
    const { data } = await api.post('/recordings/start', {
      stream_id: streamId,
      retention_days: retentionDays,
    })
    return data
  },

  async stopRecording(recordingId: string) {
    await api.post(`/recordings/${recordingId}/stop`)
  },

  async getRecording(recordingId: string) {
    const { data } = await api.get(`/recordings/${recordingId}`)
    return data
  },

  async searchRecordings(streamId: string, startDate: string, endDate: string) {
    const { data } = await api.get('/recordings/search', {
      params: { stream_id: streamId, start_date: startDate, end_date: endDate },
    })
    return data
  },

  async getTimeline(streamId: string, startDate: string, endDate: string) {
    const { data } = await api.get('/timeline', {
      params: { stream_id: streamId, start_date: startDate, end_date: endDate },
    })
    return data
  },

  async getPlaybackUrl(recordingId: string) {
    const { data } = await api.get(`/recordings/${recordingId}/playback`)
    return data
  },

  async generateThumbnails(recordingId: string, intervalSeconds: number = 60) {
    const { data } = await api.post(`/recordings/${recordingId}/thumbnails`, {
      interval_seconds: intervalSeconds,
      width: 320,
      height: 180,
    })
    return data
  },

  getHlsUrl(cameraId: string): string {
    return `http://localhost:8889/camera_${cameraId}/index.m3u8`
  },
}

// ======================================================
// AI SERVICE
// ======================================================

export const aiService = {
  async getStatus(cameraId: number) {
    const { data } = await api.get(`/ai/cameras/${cameraId}/status/`)
    return data
  },

  async startProcessing(cameraId: number) {
    const { data } = await api.post(`/ai/cameras/${cameraId}/start/`)
    return data
  },

  async stopProcessing(cameraId: number) {
    const { data } = await api.post(`/ai/cameras/${cameraId}/stop/`)
    return data
  },

  async testDetection(cameraId: number) {
    const { data } = await api.post(`/ai/cameras/${cameraId}/test/`)
    return data
  },
}

export default api

// ======================================================
// CLIPS
// ======================================================

export const clipService = {
  async list(): Promise<Clip[]> {
    const { data } = await api.get<Clip[]>('/clips')
    return data
  },

  async get(clipId: string): Promise<Clip> {
    const { data } = await api.get<Clip>(`/clips/${clipId}`)
    return data
  },

  async create(clip: ClipCreateRequest): Promise<Clip> {
    const { data } = await api.post<Clip>('/clips', clip)
    return data
  },

  async delete(clipId: string): Promise<void> {
    await api.delete(`/clips/${clipId}`)
  },

  async download(clipId: string): Promise<Blob> {
    const { data } = await api.get(`/clips/${clipId}/download`, {
      responseType: 'blob',
    })
    return data
  },
}

// ======================================================
// MOSAICOS
// ======================================================

export const mosaicoService = {
  async list(userId: string): Promise<Mosaico[]> {
    const { data } = await api.get<Mosaico[]>(`/users/${userId}/mosaics`)
    return data
  },

  async get(mosaicoId: string): Promise<Mosaico> {
    const { data } = await api.get<Mosaico>(`/mosaics/${mosaicoId}`)
    return data
  },

  async create(mosaico: MosaicoCreateRequest): Promise<Mosaico> {
    const { data } = await api.post<Mosaico>('/mosaics', mosaico)
    return data
  },

  async update(mosaicoId: string, mosaico: Partial<MosaicoCreateRequest>): Promise<Mosaico> {
    const { data } = await api.put<Mosaico>(`/mosaics/${mosaicoId}`, mosaico)
    return data
  },

  async delete(mosaicoId: string): Promise<void> {
    await api.delete(`/mosaics/${mosaicoId}`)
  },
}
