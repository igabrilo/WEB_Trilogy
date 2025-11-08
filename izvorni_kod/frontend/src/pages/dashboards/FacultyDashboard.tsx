import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import '../../css/Dashboard.css';

export default function FacultyDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="dashboard-page faculty-dashboard">
      <Header />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Dobrodošli, {user?.username || user?.firstName || 'fakultet'}!</h1>
              <p className="dashboard-subtitle">
                Promovirajte programe i povežite se sa studentima i alumnijima.
              </p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/udruge/novo')}>
                Objavi novu udrugu
              </button>
              <button className="btn-secondary" onClick={() => navigate('/profil/uredi')}>
                Uredi profil
              </button>
            </div>
          </div>

          <div className="dashboard-quick-links">
            <button className="quick-link-card" onClick={() => navigate('/fakulteti')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 8h16M8 4v16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Pregled sastavnica</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/udruge')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2"/>
                <path d="M6 20c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Studentske udruge</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/udruge/novo')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M12 8v8M8 12h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>Objavi novu udrugu</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/erasmus')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M8 12l2 2 4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span>Erasmus projekti</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/erasmus/novo')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M12 8v8M8 12h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>Objavi Erasmus projekt</span>
            </button>
          </div>

          <section className="dashboard-section">
            <h2 className="section-title">Upravljanje sadržajem</h2>
            <div className="info-grid">
              <div className="info-card">
                <div className="info-icon">📢</div>
                <h3>Promocija programa</h3>
                <p>Objavljujte i ažurirajte informacije o studijskim programima</p>
              </div>
              <div className="info-card">
                <div className="info-icon">📝</div>
                <h3>Upravljanje sadržajem</h3>
                <p>Kreirajte i uredite informacije o fakultetu i programima</p>
              </div>
              <div className="info-card">
                <div className="info-icon">👨‍🎓</div>
                <h3>Studentska usluga</h3>
                <p>Povežite se sa studentima i pružite podršku</p>
              </div>
            </div>
            <div style={{ marginTop: '24px', padding: '16px', background: '#f8fafc', borderRadius: '8px', color: '#64748b' }}>
              <strong>Napomena:</strong> Upravljačka sučelja za sastavnice bit će dodana u sljedećoj fazi.
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

