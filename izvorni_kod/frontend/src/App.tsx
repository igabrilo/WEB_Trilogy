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
import CreateAssociationPage from './pages/CreateAssociationPage';
import CreateJobPage from './pages/CreateJobPage';
import JobApplicationsPage from './pages/JobApplicationsPage';
import CreateFacultyPage from './pages/CreateFacultyPage';
import EditFacultyPage from './pages/EditFacultyPage';
import EditAssociationPage from './pages/EditAssociationPage';
import JobDetailPage from './pages/JobDetailPage';
import AdminDashboard from './pages/dashboards/AdminDashboard';
import AdminFacultiesPage from './pages/AdminFacultiesPage';
import AdminAssociationsPage from './pages/AdminAssociationsPage';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public routes (plavo) - dostupno bez prijave */}
          <Route path="/" element={<HomePage />} />
          <Route path="/fakulteti" element={<FacultiesPage />} />
          <Route path="/prakse-i-poslovi" element={<InternshipsJobsPage />} />
          <Route path="/prakse-i-poslovi/:id" element={<JobDetailPage />} />
          <Route path="/prakse-i-poslovi/novo" element={<CreateJobPage />} />
          <Route path="/prakse-i-poslovi/prijave" element={<JobApplicationsPage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/fakulteti" element={<AdminFacultiesPage />} />
          <Route path="/admin/fakulteti/novo" element={<CreateFacultyPage />} />
          <Route path="/admin/fakulteti/:slug/uredi" element={<EditFacultyPage />} />
          <Route path="/admin/udruge" element={<AdminAssociationsPage />} />
          <Route path="/udruge/:slug/uredi" element={<EditAssociationPage />} />
          <Route path="/resursi" element={<ResourcesPage />} />
          <Route path="/prijava" element={<LoginPage />} />
          <Route path="/registracija" element={<RegisterPage />} />
          <Route path="/odabir-kategorije" element={<SelectCategoryPage />} />
          <Route path="/udruge" element={<AssociationsPage />} />
          <Route path="/udruge/:slug" element={<AssociationDetailPage />} />
          <Route path="/udruge/novo" element={<CreateAssociationPage />} />
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
