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
import SelectCategoryPage from './pages/SelectCategoryPage';
import AssociationsPage from './pages/AssociationsPage';
import AssociationDetailPage from './pages/AssociationDetailPage';
import SearchResultsPage from './pages/SearchResultsPage';
import FacultyDetailPage from './pages/FacultyDetailPage';
import './css/App.css';
import StudentProfilePage from './pages/profiles/StudentProfilePage';
import AlumniProfilePage from './pages/profiles/AlumniProfilePage';
import UcenikProfilePage from './pages/profiles/UcenikProfilePage';
import EmployerProfilePage from './pages/profiles/EmployerProfilePage';
import FacultyProfilePage from './pages/profiles/FacultyProfilePage';
import KvizPage from './pages/KvizPage';

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
          <Route path="/odabir-kategorije" element={<SelectCategoryPage />} />
          <Route path="/udruge" element={<AssociationsPage />} />
          <Route path="/udruge/:slug" element={<AssociationDetailPage />} />
          <Route path="/fakulteti/:slug" element={<FacultyDetailPage />} />
          <Route path="/pretraga" element={<SearchResultsPage />} />
          {/* Profile landing pages */}
          <Route path="/profil/student" element={<StudentProfilePage />} />
          <Route path="/profil/alumni" element={<AlumniProfilePage />} />
          <Route path="/profil/ucenik" element={<UcenikProfilePage />} />
          <Route path="/profil/poslodavac" element={<EmployerProfilePage />} />
          <Route path="/profil/fakultet" element={<FacultyProfilePage />} />
          <Route path="/kviz" element={<KvizPage />} />
          
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
