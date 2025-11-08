import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import { apiService, type Association, type Faculty } from '../../services/api';
import '../../css/Dashboard.css';

export default function StudentDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [associations, setAssociations] = useState<Association[]>([]);
  const [faculties, setFaculties] = useState<Faculty[]>([]);

  useEffect(() => {
    const run = async () => {
      try {
        const [assocRes, facRes] = await Promise.all([
          apiService.getAssociations({ faculty: user?.faculty || undefined }),
          apiService.getFaculties({ q: '' })
        ]);
        
        let items = assocRes.items;
        if (user?.interests && user.interests.length > 0) {
          const interestsLower = user.interests.map(i => i.toLowerCase());
          items = items.sort((a, b) => {
            const at = (a.tags || []).map(t => t.toLowerCase());
            const bt = (b.tags || []).map(t => t.toLowerCase());
            const am = at.some(t => interestsLower.includes(t)) ? 1 : 0;
            const bm = bt.some(t => interestsLower.includes(t)) ? 1 : 0;
            return bm - am;
          });
        }
        
        setAssociations(items.slice(0, 6));
        setFaculties(facRes.items.slice(0, 6));
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      }
    };
    run();
  }, [user?.faculty, user?.interests]);

  return (
    <div className="dashboard-page student-dashboard">
      <Header />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Dobrodošao/la, {user?.firstName || 'student'}!</h1>
              <p className="dashboard-subtitle">
                Sve na jednom mjestu: prakse, fakulteti, studentske organizacije i resursi.
              </p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/prakse-i-poslovi')}>
                Prakse i poslovi
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
              <span>Prakse i poslovi</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/fakulteti')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="2"/>
                <path d="M4 8h16M8 4v16" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Fakulteti</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/udruge')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2"/>
                <path d="M6 20c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Studentske udruge</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/erasmus')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M8 12l2 2 4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span>Erasmus projekti</span>
            </button>
            <button className="quick-link-card" onClick={() => navigate('/resursi')}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="currentColor" strokeWidth="2"/>
              </svg>
              <span>Resursi</span>
            </button>
          </div>

          {associations.length > 0 && (
            <section className="dashboard-section">
              <div className="section-header">
                <h2 className="section-title">Preporučene udruge {user?.faculty ? `za ${user.faculty}` : ''}</h2>
                <Link to="/udruge" className="section-link">Vidi sve</Link>
              </div>
              <div className="dashboard-grid">
                {associations.map(a => (
                  <Link to={`/udruge/${a.slug}`} key={a.id} className="dashboard-card">
                    <div className="card-header">
                      <div className="card-logo" style={{ background: a.logoBg || '#1e293b' }}>
                        {a.logoText || (a.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase())}
                      </div>
                      {a.faculty && <span className="card-badge">{a.faculty}</span>}
                    </div>
                    <h3 className="card-title">{a.name}</h3>
                    {a.shortDescription && <p className="card-description">{a.shortDescription}</p>}
                  </Link>
                ))}
              </div>
            </section>
          )}

          {faculties.length > 0 && (
            <section className="dashboard-section">
              <div className="section-header">
                <h2 className="section-title">Izdvojeni fakulteti</h2>
                <Link to="/fakulteti" className="section-link">Vidi sve</Link>
              </div>
              <div className="dashboard-grid">
                {faculties.map(f => (
                  <Link to={`/fakulteti/${f.slug}`} key={f.slug} className="dashboard-card">
                    <div className="card-header">
                      <div className="card-logo" style={{ background: 'var(--primary-blue)' }}>
                        {f.abbreviation || f.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase()}
                      </div>
                      <span className="card-badge">{f.type === 'academy' ? 'Akademija' : 'Fakultet'}</span>
                    </div>
                    <h3 className="card-title">{f.name}</h3>
                    {f.contacts?.address && <p className="card-description">{f.contacts.address}</p>}
                  </Link>
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

