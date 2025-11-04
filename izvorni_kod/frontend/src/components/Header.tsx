import '../css/Header.css';

const Header = () => {
   return (
      <header className="header">
         <div className="header-container">
            <div className="logo">
               <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                  <rect width="32" height="32" rx="6" fill="#1e70bf" />
                  <path d="M8 12h16M8 16h16M8 20h10" stroke="white" strokeWidth="2" strokeLinecap="round" />
               </svg>
               <span className="logo-text">UNIZG Career Hub</span>
            </div>
            <nav className="nav">
               <a href="#home" className="nav-link active">Početna</a>
               <a href="#jobs" className="nav-link">Fakulteti</a>
               <a href="#internships" className="nav-link">Prakse i poslovi</a>
               <a href="#companies" className="nav-link">Profil</a>
               <a href="#about" className="nav-link">Resursi</a>
            </nav>
            <div className="header-actions">
               <button className="btn-secondary">Prijava</button>
               <button className="btn-primary">Registracija</button>
            </div>
         </div>
      </header>
   );
};

export default Header;
