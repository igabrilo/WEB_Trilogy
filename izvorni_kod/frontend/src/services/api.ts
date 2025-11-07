// For browser requests, use localhost:5001 (backend port mapped from Docker)
// The VITE_API_URL env var is for Docker internal network (backend:5000)
// But browser requests need to go through the host port 5001
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
  firstName?: string;
  lastName?: string;
  username?: string; // For employers and faculty
  role?: string;
  faculty?: string;
  interests?: string[];
}

export interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  username?: string; // For employers and faculty
  role: string;
  faculty?: string | null;
  interests?: string[];
}

export interface AuthResponse {
  success: boolean;
  message?: string;
  user?: User;
  token?: string;
  requires_aai?: boolean;
  aai_login_url?: string;
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

      // Handle non-JSON responses
      const contentType = response.headers.get('content-type');
      let data;
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        const text = await response.text();
        throw new Error(text || `HTTP ${response.status}: ${response.statusText}`);
      }

      // Special case: AAI redirect returns HTTP 200 with success: false
      // We need to check this before throwing on !response.ok
      if (data && data.requires_aai && !data.success) {
        return data; // Return AAI redirect response without throwing
      }

      if (!response.ok) {
        // Backend returns error messages in different formats
        const errorMessage = data.message || data.error || `HTTP ${response.status}: ${response.statusText}`;
        throw new Error(errorMessage);
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
    try {
      const response = await this.request<AuthResponse>('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });

      // Handle AAI redirect case (backend returns success: false but HTTP 200)
      // This is a special case - don't throw, return the response so caller can handle
      if (!response.success && response.requires_aai) {
        return response;
      }

      // For successful login, ensure success is true
      if (!response.success) {
        throw new Error(response.message || 'Login failed');
      }

      return response;
    } catch (error) {
      // Re-throw to let caller handle
      throw error;
    }
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

  async initiateGoogleLogin(): Promise<void> {
    // Redirect to backend OAuth endpoint which will redirect to Google
    const googleLoginUrl = `${this.baseURL}/api/oauth/login/google`;
    window.location.href = googleLoginUrl;
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

  // Associations management (for faculty)
  async createAssociation(data: {
    name: string;
    faculty: string;
    shortDescription: string;
    description?: string;
    type?: string;
    logoText?: string;
    logoBg?: string;
    tags?: string[];
    links?: Record<string, string>;
  }): Promise<ItemResponse<Association>> {
    return this.request<ItemResponse<Association>>('/api/associations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Jobs/Internships management (for employers)
  async createJob(data: {
    title: string;
    description: string;
    type: 'internship' | 'job' | 'part-time' | 'remote';
    company?: string;
    location?: string;
    salary?: string;
    requirements?: string[];
    tags?: string[];
  }): Promise<ItemResponse<Job>> {
    return this.request<ItemResponse<Job>>('/api/jobs', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getJobs(params?: { type?: string; q?: string }): Promise<ListResponse<Job>> {
    const qs = new URLSearchParams();
    if (params?.type) qs.append('type', params.type);
    if (params?.q) qs.append('q', params.q);
    const qp = qs.toString();
    return this.request<ListResponse<Job>>(`/api/jobs${qp ? `?${qp}` : ''}`);
  }

  async getJob(jobId: number): Promise<ItemResponse<Job>> {
    return this.request<ItemResponse<Job>>(`/api/jobs/${jobId}`);
  }

  async applyToJob(jobId: number, message?: string): Promise<ItemResponse<JobApplication>> {
    return this.request<ItemResponse<JobApplication>>(`/api/jobs/${jobId}/apply`, {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async getJobApplications(jobId?: number): Promise<ListResponse<JobApplication>> {
    const endpoint = jobId ? `/api/jobs/${jobId}/applications` : '/api/jobs/applications';
    return this.request<ListResponse<JobApplication>>(endpoint);
  }

  async updateApplicationStatus(applicationId: number, status: 'pending' | 'approved' | 'rejected'): Promise<ItemResponse<JobApplication>> {
    return this.request<ItemResponse<JobApplication>>(`/api/jobs/applications/${applicationId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async sendEmailToApplicant(applicationId: number, subject: string, message: string): Promise<{ success: boolean; message: string; email: any }> {
    return this.request(`/api/jobs/applications/${applicationId}/send-email`, {
      method: 'POST',
      body: JSON.stringify({ subject, message }),
    });
  }

  // Erasmus Projects API
  async createErasmusProject(data: {
    title: string;
    description: string;
    facultySlug: string;
    country?: string;
    university?: string;
    fieldOfStudy?: string;
    duration?: string;
    applicationDeadline?: string;
    requirements?: string[];
    benefits?: string[];
    contactEmail?: string;
    contactPhone?: string;
    website?: string;
  }): Promise<ItemResponse<ErasmusProject>> {
    return this.request<ItemResponse<ErasmusProject>>('/api/erasmus', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getErasmusProjects(params?: { faculty?: string; fieldOfStudy?: string }): Promise<ListResponse<ErasmusProject>> {
    const qs = new URLSearchParams();
    if (params?.faculty) qs.append('faculty', params.faculty);
    if (params?.fieldOfStudy) qs.append('fieldOfStudy', params.fieldOfStudy);
    const qp = qs.toString();
    return this.request<ListResponse<ErasmusProject>>(`/api/erasmus${qp ? `?${qp}` : ''}`);
  }

  async getErasmusProject(projectId: number): Promise<ItemResponse<ErasmusProject>> {
    return this.request<ItemResponse<ErasmusProject>>(`/api/erasmus/${projectId}`);
  }

  async updateErasmusProject(projectId: number, data: Partial<ErasmusProject>): Promise<ItemResponse<ErasmusProject>> {
    return this.request<ItemResponse<ErasmusProject>>(`/api/erasmus/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteErasmusProject(projectId: number): Promise<{ success: boolean; message: string }> {
    return this.request(`/api/erasmus/${projectId}`, {
      method: 'DELETE',
    });
  }

  // Favorites API
  async addFavoriteFaculty(facultySlug: string): Promise<ItemResponse<FavoriteFaculty>> {
    return this.request<ItemResponse<FavoriteFaculty>>('/api/favorites/faculties', {
      method: 'POST',
      body: JSON.stringify({ facultySlug: facultySlug }),
    });
  }

  async getFavoriteFaculties(): Promise<ListResponse<FavoriteFaculty>> {
    return this.request<ListResponse<FavoriteFaculty>>('/api/favorites/faculties');
  }

  async removeFavoriteFaculty(facultySlug: string): Promise<{ success: boolean; message: string }> {
    return this.request(`/api/favorites/faculties/${facultySlug}`, {
      method: 'DELETE',
    });
  }

  async checkFavoriteFaculty(facultySlug: string): Promise<{ success: boolean; isFavorite: boolean }> {
    return this.request<{ success: boolean; isFavorite: boolean }>(`/api/favorites/faculties/${facultySlug}/check`);
  }

  // Profile update API
  async updateProfile(data: {
    firstName?: string;
    lastName?: string;
    username?: string;
    faculty?: string;
    interests?: string[];
  }): Promise<ItemResponse<User>> {
    return this.request<ItemResponse<User>>('/api/auth/me', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Admin endpoints
  async createFaculty(data: {
    name: string;
    type: 'faculty' | 'academy';
    abbreviation?: string;
    email?: string;
    phone?: string;
    address?: string;
    website?: string;
  }): Promise<ItemResponse<Faculty>> {
    return this.request<ItemResponse<Faculty>>('/api/admin/faculties', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getAllFaculties(): Promise<ListResponse<Faculty>> {
    return this.request<ListResponse<Faculty>>('/api/admin/faculties');
  }

  async updateFaculty(slug: string, data: {
    name?: string;
    type?: 'faculty' | 'academy';
    abbreviation?: string;
    email?: string;
    phone?: string;
    address?: string;
    website?: string;
  }): Promise<ItemResponse<Faculty>> {
    return this.request<ItemResponse<Faculty>>(`/api/admin/faculties/${slug}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteFaculty(slug: string): Promise<{ success: boolean; message: string }> {
    return this.request(`/api/admin/faculties/${slug}`, {
      method: 'DELETE',
    });
  }

  async getAllAssociations(): Promise<ListResponse<Association>> {
    return this.request<ListResponse<Association>>('/api/admin/associations');
  }

  async updateAssociation(associationId: number, data: Partial<Association>): Promise<ItemResponse<Association>> {
    return this.request<ItemResponse<Association>>(`/api/admin/associations/${associationId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteAssociation(associationId: number): Promise<{ success: boolean; message: string }> {
    return this.request(`/api/admin/associations/${associationId}`, {
      method: 'DELETE',
    });
  }

  // Chatbot methods
  async sendChatbotMessage(message: string, sessionId?: string, provider: string = 'smotra'): Promise<ChatbotResponse> {
    return this.request<ChatbotResponse>('/api/chatbot/send', {
      method: 'POST',
      body: JSON.stringify({ message, session_id: sessionId, provider }),
    });
  }

  async getChatbotHistory(sessionId?: string): Promise<{ success: boolean; messages: ChatMessage[]; session_id?: string }> {
    const qs = new URLSearchParams();
    if (sessionId) qs.append('session_id', sessionId);
    return this.request(`/api/chatbot/history${qs.toString() ? `?${qs.toString()}` : ''}`);
  }

  async createChatbotSession(): Promise<{ success: boolean; session_id: string }> {
    return this.request('/api/chatbot/session', {
      method: 'POST',
    });
  }

  async deleteChatbotSession(sessionId: string): Promise<{ success: boolean; message: string }> {
    return this.request(`/api/chatbot/session/${sessionId}`, {
      method: 'DELETE',
    });
  }

  async getChatbotProviders(): Promise<{ success: boolean; providers: string[] }> {
    return this.request('/api/chatbot/providers');
  }

  // Faculty Inquiries
  async sendFacultyInquiry(data: {
    facultySlug: string;
    senderName: string;
    senderEmail: string;
    subject: string;
    message: string;
  }): Promise<ItemResponse<FacultyInquiry>> {
    return this.request<ItemResponse<FacultyInquiry>>('/api/inquiries/faculties', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getFacultyInquiries(facultySlug: string, status?: string): Promise<ListResponse<FacultyInquiry>> {
    const qs = new URLSearchParams();
    if (status) qs.append('status', status);
    const qp = qs.toString();
    return this.request<ListResponse<FacultyInquiry>>(`/api/inquiries/faculties/${facultySlug}${qp ? `?${qp}` : ''}`);
  }

  async getMyInquiries(): Promise<ListResponse<FacultyInquiry>> {
    return this.request<ListResponse<FacultyInquiry>>('/api/inquiries/my');
  }

  async markInquiryRead(inquiryId: number): Promise<ItemResponse<FacultyInquiry>> {
    return this.request<ItemResponse<FacultyInquiry>>(`/api/inquiries/${inquiryId}/read`, {
      method: 'PUT',
    });
  }

  async replyToInquiry(inquiryId: number, replyMessage: string): Promise<ItemResponse<FacultyInquiry>> {
    return this.request<ItemResponse<FacultyInquiry>>(`/api/inquiries/${inquiryId}/reply`, {
      method: 'POST',
      body: JSON.stringify({ replyMessage }),
    });
  }
}

export interface Job {
  id: number;
  title: string;
  description: string;
  type: 'internship' | 'job' | 'part-time' | 'remote';
  company?: string;
  location?: string;
  salary?: string;
  requirements?: string[];
  tags?: string[];
  createdAt?: string;
  status?: string;
  applicationCount?: number;
}

export interface JobApplication {
  id: number;
  jobId: number;
  userId: number;
  userEmail: string;
  message?: string;
  status: 'pending' | 'approved' | 'rejected';
  createdAt?: string;
  updatedAt?: string;
  user?: User;
  job?: {
    id: number;
    title: string;
    type: string;
  };
}

export interface ErasmusProject {
  id: number;
  title: string;
  description: string;
  facultySlug: string;
  facultyName?: string;
  country?: string;
  university?: string;
  fieldOfStudy?: string;
  duration?: string;
  applicationDeadline?: string;
  requirements?: string[];
  benefits?: string[];
  contactEmail?: string;
  contactPhone?: string;
  website?: string;
  status: 'active' | 'archived';
  createdBy: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface FavoriteFaculty {
  id: number;
  userId: number;
  facultySlug: string;
  facultyName?: string;
  createdAt?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  message: string;
  timestamp?: string;
}

export interface ChatbotResponse {
  success: boolean;
  message?: string;
  session_id?: string;
  provider?: string;
  error?: string;
}

export interface ChatbotSession {
  session_id: string;
  messages: ChatMessage[];
  created_at?: string;
}

export interface FacultyInquiry {
  id: number;
  facultySlug: string;
  userId?: number;
  senderName: string;
  senderEmail: string;
  subject: string;
  message: string;
  status: 'pending' | 'read' | 'replied';
  createdAt: string;
  readAt?: string | null;
  repliedAt?: string | null;
  replyMessage?: string | null;
  faculty?: Faculty;
  user?: User;
}

export const apiService = new ApiService();

