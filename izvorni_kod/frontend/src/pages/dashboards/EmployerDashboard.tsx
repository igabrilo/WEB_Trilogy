import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import '../../css/Dashboard.css';

export default function EmployerDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="dashboard-page employer-dashboard">
      <Header />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Dobrodošli, {user?.username || user?.firstName || 'poslodavac'}!</h1>
              <p className="dashboard-subtitle">
                Objavite oglase, istražite profile kandidata i povežite se sa zajednicom.
              </p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/prakse-i-poslovi/novo')}>
                Objavi praksu/posao
              </button>
              <button className="btn-secondary" onClick={() => navigate('/prakse-i-poslovi/prijave')}>
                Pregled prijava
              </button>
              <button className="btn-secondary" onClick={() => navigate('/profil/uredi')}>
                Uredi profil
              </button>
            </div>
          </div>

          <div className="dashboard-quick-links">
            <button className="quick-link-card" onClick={() => navigate('/prakse-i-poslovi/novo')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M12 8v8M8 12h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>Objavi oglas</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/prakse-i-poslovi/prijave')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="6" width="16" height="12" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 10h16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Pregled prijava</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/prakse-i-poslovi')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                <path d="m21 21-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Pretraži oglase</span>
            </button>
          </div>

          <section className="dashboard-section">
            <h2 className="section-title">Brzi pristup</h2>
            <div className="info-grid">
              <div className="info-card">
                <div className="info-icon">📋</div>
                <h3>Upravljanje oglasima</h3>
                <p>Kreirajte, uredite i upravljajte oglasima za prakse i poslove</p>
              </div>
              <div className="info-card">
                <div className="info-icon">👥</div>
                <h3>Pregled kandidata</h3>
                <p>Pretražite i filtrirate profile studenata i alumnija</p>
              </div>
              <div className="info-card">
                <div className="info-icon">📊</div>
                <h3>Statistike</h3>
                <p>Pratite performanse oglasa i aplikacija</p>
              </div>
            </div>
            <div style={{ marginTop: '24px', padding: '16px', background: '#f8fafc', borderRadius: '8px', color: '#64748b' }}>
              <strong>Napomena:</strong> Napredni HR alati bit će dodani u sljedećoj fazi.
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

