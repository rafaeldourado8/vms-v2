import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

type PendingRequest = {
  resolve: (value?: any) => void;
  reject: (error?: any) => void;
  config: AxiosRequestConfig;
};

const api: AxiosInstance = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, 
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    const tenantId = localStorage.getItem('tenant_id');
    
    if (token) {
      config.headers = config.headers ?? {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    if (tenantId) {
      config.headers = config.headers ?? {};
      config.headers['X-Tenant-ID'] = tenantId;
    }
    
    return config;
  },
  (error) => Promise.reject(error),
);

let isRefreshing = false;
let failedQueue: PendingRequest[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((p) => {
    if (error) {
      p.reject(error);
    } else {
      if (token) {
        p.config.headers = p.config.headers ?? {};
        p.config.headers['Authorization'] = `Bearer ${token}`;
        p.resolve(api(p.config));
      } else {
        p.resolve(api(p.config));
      }
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError & { config?: AxiosRequestConfig }) => {
    const originalConfig = error?.config;

    if (!originalConfig || error?.response?.status !== 401) {
      return Promise.reject(error);
    }

    if ((originalConfig as any)._retry) {
      return Promise.reject(error);
    }

    (originalConfig as any)._retry = true;

    try {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject, config: originalConfig });
        });
      }

      isRefreshing = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(error);
      }

      const plain = axios.create({
        baseURL: API_BASE,
        withCredentials: true,
        headers: { 'Content-Type': 'application/json' },
      });

      const resp = await plain.post('/admin/auth/refresh/', { refresh: refreshToken });

      const newAccess = resp.data?.access;
      if (!newAccess) {
        throw new Error('Refresh failed');
      }

      localStorage.setItem('token', newAccess);
      processQueue(null, newAccess);

      originalConfig.headers = originalConfig.headers ?? {};
      originalConfig.headers['Authorization'] = `Bearer ${newAccess}`;

      return api(originalConfig);
    } catch (refreshError) {
      processQueue(refreshError, null);
      localStorage.clear();
      window.location.href = '/login';
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  },
);

export default api;