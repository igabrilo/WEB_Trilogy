import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import { apiService, type Faculty, type Association } from '../../services/api';
import '../../css/Dashboard.css';

export default function AdminDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [associations, setAssociations] = useState<Association[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?.role !== 'admin') {
      navigate('/');
      return;
    }

    const loadData = async () => {
      try {
        const [facRes, assocRes] = await Promise.all([
          apiService.getAllFaculties(),
          apiService.getAllAssociations(),
        ]);
        setFaculties(facRes.items);
        setAssociations(assocRes.items);
      } catch (error) {
        console.error('Error loading admin data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [user, navigate]);

  if (loading) {
    return (
      <div className="dashboard-page">
        <Header />
        <main className="dashboard-main">
          <div className="dashboard-container">
            <p>Učitavanje...</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="dashboard-page admin-dashboard">
      <Header />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Admin Panel</h1>
              <p className="dashboard-subtitle">
                Upravljajte fakultetima, studentskim udrugama i svim sadržajem sustava.
              </p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/admin/fakulteti/novo')}>
                Dodaj fakultet
              </button>
              <button className="btn-primary" onClick={() => navigate('/udruge/novo')}>
                Dodaj udrugu
              </button>
            </div>
          </div>

          <div className="dashboard-quick-links">
            <button className="quick-link-card" onClick={() => navigate('/admin/fakulteti')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 8h16M8 4v16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Upravljaj fakultetima</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/admin/udruge')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2"/>
                <path d="M6 20c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Upravljaj udrugama</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/prakse-i-poslovi')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="6" width="16" height="12" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 10h16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Pregled oglasa</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/pretraga')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                <path d="m21 21-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Pretraga</span>
            </button>
          </div>

          <section className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">Fakulteti ({faculties.length})</h2>
              <Link to="/admin/fakulteti/novo" className="section-link">Dodaj novi</Link>
            </div>
            <div className="dashboard-grid">
              {faculties.slice(0, 6).map(f => (
                <div key={f.slug} className="dashboard-card">
                  <div className="card-header">
                    <div className="card-logo" style={{ background: 'var(--primary-blue)' }}>
                      {f.abbreviation || f.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase()}
                    </div>
                    <span className="card-badge">{f.type === 'academy' ? 'Akademija' : 'Fakultet'}</span>
                  </div>
                  <h3 className="card-title">{f.name}</h3>
                  {f.contacts?.address && <p className="card-description">{f.contacts.address}</p>}
                  <div style={{ marginTop: '0.75rem', display: 'flex', gap: '0.5rem' }}>
                    <Link to={`/admin/fakulteti/${f.slug}/uredi`} className="btn-secondary" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}>
                      Uredi
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">Studentske udruge ({associations.length})</h2>
              <Link to="/udruge/novo" className="section-link">Dodaj novu</Link>
            </div>
            <div className="dashboard-grid">
              {associations.slice(0, 6).map(a => (
                <div key={a.id} className="dashboard-card">
                  <div className="card-header">
                    <div className="card-logo" style={{ background: a.logoBg || '#1e293b' }}>
                      {a.logoText || (a.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase())}
                    </div>
                    {a.faculty && <span className="card-badge">{a.faculty}</span>}
                  </div>
                  <h3 className="card-title">{a.name}</h3>
                  {a.shortDescription && <p className="card-description">{a.shortDescription}</p>}
                  <div style={{ marginTop: '0.75rem', display: 'flex', gap: '0.5rem' }}>
                    <Link to={`/udruge/${a.slug}/uredi`} className="btn-secondary" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}>
                      Uredi
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

