import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import '../../css/Dashboard.css';

export default function UcenikDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="dashboard-page ucenik-dashboard">
      <Header />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Dobrodošao/la, {user?.firstName || 'učenik'}!</h1>
              <p className="dashboard-subtitle">
                Istraži fakultete i pripremi se za odabir studija.
              </p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/fakulteti')}>
                Istraži fakultete
              </button>
              <button className="btn-secondary" onClick={() => navigate('/profil')}>
                Moj profil
              </button>
            </div>
          </div>

          <div className="dashboard-quick-links">
            <button className="quick-link-card" onClick={() => navigate('/fakulteti')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 8h16M8 4v16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Fakulteti</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/kviz')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M12 8v8M8 12h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>Kviz profesionalne orijentacije</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/resursi')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Korisni resursi</span>
            </button>
          </div>

          <section className="dashboard-section">
            <h2 className="section-title">Što te očekuje u kvizu?</h2>
            <div className="info-grid">
              <div className="info-card">
                <div className="info-icon">❓</div>
                <h3>Pitanja o interesima</h3>
                <p>Odgovori na pitanja o svojim interesima i vještinama</p>
              </div>
              <div className="info-card">
                <div className="info-icon">💡</div>
                <h3>Prijedlozi područja</h3>
                <p>Dobij personalizirane prijedloge studijskih programa</p>
              </div>
              <div className="info-card">
                <div className="info-icon">📚</div>
                <h3>Savjeti za upis</h3>
                <p>Korisni savjeti za pripremu i upis na fakultet</p>
              </div>
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

