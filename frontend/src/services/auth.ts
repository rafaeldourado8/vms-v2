import api from '@/lib/axios';

interface LoginCredentials {
  username: string;
  password: string;
}

interface AuthResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    tenant_id: string;
    role: string;
  };
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post('/v1/auth/login', {
      email: credentials.username,
      password: credentials.password
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      localStorage.setItem('tenant_id', response.data.user.tenant_id || 'default');
    }
    
    return response.data;
  }

  async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      throw new Error('No refresh token');
    }

    const response = await api.post('/v1/auth/refresh', {
      refresh: refreshToken
    });

    if (response.data.access) {
      localStorage.setItem('token', response.data.access);
    }

    return response.data.access;
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('tenant_id');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getTenantId(): string | null {
    return localStorage.getItem('tenant_id');
  }

  getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export default new AuthService();
