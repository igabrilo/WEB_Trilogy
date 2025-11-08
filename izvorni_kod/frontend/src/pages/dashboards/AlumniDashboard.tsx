import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import { apiService, type Faculty } from '../../services/api';
import '../../css/Dashboard.css';

export default function AlumniDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [faculties, setFaculties] = useState<Faculty[]>([]);

  useEffect(() => {
    const run = async () => {
      try {
        const res = await apiService.getFaculties();
        setFaculties(res.items.slice(0, 6));
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      }
    };
    run();
  }, []);

  return (
    <div className="dashboard-page alumni-dashboard">
      <Header />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Dobrodošao/la, {user?.firstName || 'alumni'}!</h1>
              <p className="dashboard-subtitle">
                Pronađi poslove i projekte, poveži se s alumnijima i mentoriraj studente.
              </p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/prakse-i-poslovi')}>
                Pronađi posao
              </button>
              <button className="btn-secondary" onClick={() => navigate('/profil')}>
                Moj profil
              </button>
            </div>
          </div>

          <div className="dashboard-quick-links">
            <button className="quick-link-card" onClick={() => navigate('/prakse-i-poslovi')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="6" width="16" height="12" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 10h16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Poslovi i projekti</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/fakulteti')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 8h16M8 4v16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Fakulteti</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/pretraga?q=alumni')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2"/>
                <path d="M6 20c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Alumni mreža</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/resursi')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Resursi</span>
            </button>
          </div>

          {faculties.length > 0 && (
            <section className="dashboard-section">
              <div className="section-header">
                <h2 className="section-title">Brzi kontakti fakulteta i akademija</h2>
                <Link to="/fakulteti" className="section-link">Vidi sve</Link>
              </div>
              <div className="dashboard-grid">
                {faculties.map(f => (
                  <div key={f.slug} className="dashboard-card">
                    <div className="card-header">
                      <div className="card-logo" style={{ background: 'var(--primary-blue)' }}>
                        {f.abbreviation || f.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase()}
                      </div>
                      <span className="card-badge">{f.type === 'academy' ? 'Akademija' : 'Fakultet'}</span>
                    </div>
                    <h3 className="card-title">{f.name}</h3>
                    <div className="card-contacts">
                      {f.contacts?.website && (
                        <a href={f.contacts.website} target="_blank" rel="noreferrer" className="contact-link">
                          🌐 Web stranica
                        </a>
                      )}
                      {f.contacts?.email && (
                        <a href={`mailto:${f.contacts.email}`} className="contact-link">
                          ✉️ {f.contacts.email}
                        </a>
                      )}
                      {f.contacts?.phone && (
                        <a href={`tel:${f.contacts.phone.replace(/\s+/g, '')}`} className="contact-link">
                          📞 {f.contacts.phone}
                        </a>
                      )}
                      {f.contacts?.address && (
                        <div className="contact-item">📍 {f.contacts.address}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

