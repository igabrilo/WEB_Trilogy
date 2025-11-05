import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../css/Header.css';
import logoImage from '../assets/tamnoplavi.png';

const Header = () => {
   const location = useLocation();
   const navigate = useNavigate();
   const { user, isAuthenticated, logout } = useAuth();

   const isActive = (path: string) => {
      if (path === '/' && location.pathname === '/') return 'active';
      if (path !== '/' && location.pathname.startsWith(path)) return 'active';
      return '';
   };

   const handleLogout = async () => {
      try {
         await logout();
         navigate('/');
      } catch (error) {
         console.error('Logout error:', error);
      }
   };

   return (
      <header className="header">
         <div className="header-container">
            <Link to="/" className="logo">
               <img src={logoImage} alt="UNIZG Logo" className="logo-image" />
               <span className="logo-text">
                  <span>UNIZG</span>
                  <span>Career</span>
                  <span>Hub</span>
               </span>
            </Link>
            <nav className="nav">
               <Link to="/" className={`nav-link ${isActive('/')}`}>Početna</Link>
               <Link to="/fakulteti" className={`nav-link ${isActive('/fakulteti')}`}>Fakulteti</Link>
               <Link to="/udruge" className={`nav-link ${isActive('/udruge')}`}>Udruge</Link>
               <Link to="/prakse-i-poslovi" className={`nav-link ${isActive('/prakse-i-poslovi')}`}>Prakse i poslovi</Link>
               <Link to="/resursi" className={`nav-link ${isActive('/resursi')}`}>Resursi</Link>
               {isAuthenticated && (
                  <Link to="/profil" className={`nav-link ${isActive('/profil')}`}>Profil</Link>
               )}
            </nav>
            <div className="header-actions">
               {isAuthenticated ? (
                  <>
                     <span className="user-greeting">
                        Zdravo, {user?.firstName}!
                     </span>
                     <button onClick={handleLogout} className="btn-secondary">
                        Odjava
                     </button>
                  </>
               ) : (
                  <>
                     <Link to="/prijava" className="btn-secondary">Prijava</Link>
                     <Link to="/registracija" className="btn-primary">Registracija</Link>
                  </>
               )}
            </div>
         </div>
      </header>
   );
};

export default Header;
