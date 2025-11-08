import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { apiService, type LoginCredentials, type RegisterData, type User } from '../services/api';

interface AuthContextType {
   user: User | null;
   isAuthenticated: boolean;
   isLoading: boolean;
   login: (credentials: LoginCredentials) => Promise<void>;
   register: (data: RegisterData) => Promise<void>;
   logout: () => Promise<void>;
   refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
   const context = useContext(AuthContext);
   if (context === undefined) {
      throw new Error('useAuth must be used within an AuthProvider');
   }
   return context;
};

interface AuthProviderProps {
   children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
   const [user, setUser] = useState<User | null>(null);
   const [isLoading, setIsLoading] = useState<boolean>(true);

   // Initialize user from localStorage on mount
   useEffect(() => {
      const initializeAuth = async () => {
         const token = localStorage.getItem('token');
         const storedUser = localStorage.getItem('user');

         if (token && storedUser) {
            try {
               // Validate token by fetching current user
               const currentUser = await apiService.getCurrentUser();
               setUser(currentUser);
            } catch (error) {
               // Token is invalid, clear storage
               localStorage.removeItem('token');
               localStorage.removeItem('user');
               setUser(null);
            }
         }
         setIsLoading(false);
      };

      initializeAuth();
   }, []);

   const login = async (credentials: LoginCredentials) => {
      try {
         const response = await apiService.login(credentials);

         if (response.success && response.token && response.user) {
            localStorage.setItem('token', response.token);
            localStorage.setItem('user', JSON.stringify(response.user));
            setUser(response.user);
         } else {
            throw new Error(response.message || 'Login failed');
         }
      } catch (error) {
         throw error;
      }
   };

   const register = async (data: RegisterData) => {
      try {
         const response = await apiService.register(data);

         if (response.success && response.token && response.user) {
            localStorage.setItem('token', response.token);
            localStorage.setItem('user', JSON.stringify(response.user));
            setUser(response.user);
         } else {
            throw new Error(response.message || 'Registration failed');
         }
      } catch (error) {
         throw error;
      }
   };

   const logout = async () => {
      try {
         await apiService.logout();
         setUser(null);
      } catch (error) {
         // Even if logout fails, clear local state
         localStorage.removeItem('token');
         localStorage.removeItem('user');
         setUser(null);
      }
   };

   const refreshUser = async () => {
      try {
         const currentUser = await apiService.getCurrentUser();
         setUser(currentUser);
         localStorage.setItem('user', JSON.stringify(currentUser));
      } catch (error) {
         // If refresh fails, user might be logged out
         localStorage.removeItem('token');
         localStorage.removeItem('user');
         setUser(null);
         throw error;
      }
   };

   const value: AuthContextType = {
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      register,
      logout,
      refreshUser,
   };

   return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

