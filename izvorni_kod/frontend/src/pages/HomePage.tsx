import Header from '../components/Header';
import Hero from '../components/Hero';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import StudentDashboard from './dashboards/StudentDashboard';
import AlumniDashboard from './dashboards/AlumniDashboard';
import UcenikDashboard from './dashboards/UcenikDashboard';
import EmployerDashboard from './dashboards/EmployerDashboard';
import FacultyDashboard from './dashboards/FacultyDashboard';
import AdminDashboard from './dashboards/AdminDashboard';

const HomePage = () => {
   const { isAuthenticated, user, isLoading } = useAuth();

   // Show loading state while checking authentication
   if (isLoading) {
      return (
         <div className="home-page">
            <Header />
            <main style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
               <div>Učitavanje...</div>
            </main>
            <Footer />
         </div>
      );
   }

   // If user is authenticated, show role-specific dashboard
   if (isAuthenticated && user) {
      switch (user.role) {
         case 'student':
            return <StudentDashboard />;
         case 'alumni':
            return <AlumniDashboard />;
         case 'ucenik':
            return <UcenikDashboard />;
         case 'employer':
         case 'poslodavac':
            return <EmployerDashboard />;
         case 'faculty':
         case 'fakultet':
            return <FacultyDashboard />;
         case 'admin':
            return <AdminDashboard />;
         default:
            // Unknown role, show generic home
            return (
               <div className="home-page">
                  <Header />
                  <Hero />
                  <Footer />
               </div>
            );
      }
   }

   // Not authenticated - show generic home page
   return (
      <div className="home-page">
         <Header />
         <Hero />
         <Footer />
      </div>
   );
};

export default HomePage;
