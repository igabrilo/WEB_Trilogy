import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import HomePage from './pages/HomePage';
import FacultiesPage from './pages/FacultiesPage';
import InternshipsJobsPage from './pages/InternshipsJobsPage';
import ProfilePage from './pages/ProfilePage';
import ResourcesPage from './pages/ResourcesPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import './css/App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public routes (plavo) - dostupno bez prijave */}
          <Route path="/" element={<HomePage />} />
          <Route path="/fakulteti" element={<FacultiesPage />} />
          <Route path="/prakse-i-poslovi" element={<InternshipsJobsPage />} />
          <Route path="/resursi" element={<ResourcesPage />} />
          <Route path="/prijava" element={<LoginPage />} />
          <Route path="/registracija" element={<RegisterPage />} />
          
          {/* Protected routes (bijelo) - zahtijevaju autentifikaciju */}
          <Route 
            path="/profil" 
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
