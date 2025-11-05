// For browser requests, use localhost:5001 (host port mapping)
// The VITE_API_URL env var is for Docker internal network (backend:5000)
// But browser requests need to go through the host port
const API_URL = import.meta.env.VITE_API_URL?.includes('localhost') 
  ? import.meta.env.VITE_API_URL 
  : 'http://localhost:5001';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role?: string;
  faculty?: string;
  interests?: string[];
}

export interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  role: string;
   faculty?: string | null;
   interests?: string[];
}

export interface AuthResponse {
  success: boolean;
  message?: string;
  user?: User;
  token?: string;
}

export interface Association {
  id: number;
  slug: string;
  name: string;
  faculty?: string;
  type?: string;
  logoText?: string;
  logoBg?: string;
  shortDescription?: string;
  description?: string;
  tags?: string[];
  links?: Record<string, string>;
}

export interface ListResponse<T> {
  success: boolean;
  count: number;
  items: T[];
}

export interface ItemResponse<T> {
  success: boolean;
  item: T;
}

export interface SearchResults {
  success: boolean;
  query: string;
  results: {
    associations: Association[];
    faculties: Faculty[];
  }
}

export interface FacultyContacts {
  email?: string | null;
  phone?: string | null;
  address?: string | null;
  website?: string | null;
}

export interface Faculty {
  slug: string;
  name: string;
  abbreviation?: string;
  type: 'faculty' | 'academy';
  contacts?: FacultyContacts;
}

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'An error occurred');
      }

      return data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Network error occurred');
    }
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    return this.request<AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async register(data: RegisterData): Promise<AuthResponse> {
    return this.request<AuthResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/api/auth/me');
  }

  async logout(): Promise<void> {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  async getAssociations(params?: { faculty?: string; q?: string }): Promise<ListResponse<Association>> {
    const qs = new URLSearchParams();
    if (params?.faculty) qs.append('faculty', params.faculty);
    if (params?.q) qs.append('q', params.q);
    const qp = qs.toString();
    return this.request<ListResponse<Association>>(`/api/associations${qp ? `?${qp}` : ''}`);
  }

  async getAssociation(slug: string): Promise<ItemResponse<Association>> {
    return this.request<ItemResponse<Association>>(`/api/associations/${slug}`);
  }

  async searchAll(params: { q: string; faculty?: string }): Promise<SearchResults> {
    const qs = new URLSearchParams();
    qs.append('q', params.q);
    if (params.faculty) qs.append('faculty', params.faculty);
    return this.request<SearchResults>(`/api/search?${qs.toString()}`);
  }

  async getFaculties(params?: { q?: string }): Promise<ListResponse<Faculty>> {
    const qs = new URLSearchParams();
    if (params?.q) qs.append('q', params.q);
    const qp = qs.toString();
    return this.request<ListResponse<Faculty>>(`/api/faculties${qp ? `?${qp}` : ''}`);
  }

  async getFaculty(slug: string): Promise<ItemResponse<Faculty>> {
    return this.request<ItemResponse<Faculty>>(`/api/faculties/${slug}`);
  }
}

export const apiService = new ApiService();

