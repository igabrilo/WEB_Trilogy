import { useEffect, useMemo, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type Association, type Faculty } from '../services/api';
import '../css/FacultyDetailPage.css';

const colorFromSlug = (slug: string) => {
  // Simple hash to color for deterministic gradient
  let hash = 0;
  for (let i = 0; i < slug.length; i++) hash = slug.charCodeAt(i) + ((hash << 5) - hash);
  const hue = Math.abs(hash) % 360;
  return `linear-gradient(180deg, hsl(${hue} 70% 55%) 0%, hsl(${(hue + 20) % 360} 70% 45%) 100%)`;
};

export default function FacultyDetailPage() {
  const { slug = '' } = useParams();
  const navigate = useNavigate();
  const [faculty, setFaculty] = useState<Faculty | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<'pregled' | 'udruge'>('pregled');
  const [associations, setAssociations] = useState<Association[]>([]);

  useEffect(() => {
    const run = async () => {
      try {
        const res = await apiService.getFaculty(slug);
        setFaculty(res.item);
      } finally {
        setLoading(false);
      }
    };
    run();
  }, [slug]);

  useEffect(() => {
    const loadAssociations = async () => {
      if (!faculty?.abbreviation) return;
      const res = await apiService.getAssociations({ faculty: faculty.abbreviation });
      setAssociations(res.items || []);
    };
    if (tab === 'udruge') loadAssociations();
  }, [tab, faculty?.abbreviation]);

  const coverStyle = useMemo(() => ({ background: colorFromSlug(slug) }), [slug]);
  const logoText = faculty?.abbreviation || faculty?.name?.split(' ').map(w => w[0]).slice(0,3).join('').toUpperCase();

  return (
    <div className="faculty-detail-page">
      <Header />
      <main>
        {loading && (
          <div className="container" style={{ padding: '2rem 1rem' }}>Učitavanje...</div>
        )}
        {!loading && !faculty && (
          <div className="container" style={{ padding: '2rem 1rem' }}>Fakultet nije pronađen.</div>
        )}
        {!loading && faculty && (
          <>
            <section className="faculty-cover" style={coverStyle}>
              <div className="faculty-cover-inner container">
                <div className="faculty-avatar" aria-hidden>{logoText}</div>
                <div>
                  <h1 className="faculty-title">{faculty.name}</h1>
                  <div className="faculty-meta">
                    <span className="pill">{faculty.type === 'academy' ? 'Akademija' : 'Fakultet'}</span>
                    {faculty.abbreviation && <span className="pill pill-light">{faculty.abbreviation}</span>}
                  </div>
                </div>
              </div>
            </section>

            <section className="container" style={{ padding: '1rem' }}>
              <nav className="faculty-tabs">
                <button className={`tab ${tab === 'pregled' ? 'active' : ''}`} onClick={() => setTab('pregled')}>Pregled</button>
                <button className={`tab ${tab === 'udruge' ? 'active' : ''}`} onClick={() => setTab('udruge')}>Udruge</button>
              </nav>

              {tab === 'pregled' && (
                <div className="faculty-about">
                  <div className="contacts">
                    {faculty.contacts?.website && (
                      <a className="contact" href={faculty.contacts.website} target="_blank" rel="noreferrer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M3 12a9 9 0 1 0 18 0A9 9 0 0 0 3 12Zm5 0a4 4 0 1 0 8 0 4 4 0 0 0-8 0Z" stroke="currentColor" strokeWidth="1.5"/></svg>
                        {faculty.contacts.website}
                      </a>
                    )}
                    {faculty.contacts?.email && (
                      <a className="contact" href={`mailto:${faculty.contacts.email}`}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M4 6h16v12H4z" stroke="currentColor" strokeWidth="1.5"/><path d="m4 6 8 6 8-6" stroke="currentColor" strokeWidth="1.5"/></svg>
                        {faculty.contacts.email}
                      </a>
                    )}
                    {faculty.contacts?.phone && (
                      <a className="contact" href={`tel:${faculty.contacts.phone.replace(/\s+/g,'')}`}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M6 2h4l2 5-3 2a11 11 0 0 0 6 6l2-3 5 2v4a3 3 0 0 1-3 3c-10 0-18-8-18-18a3 3 0 0 1 3-3Z" stroke="currentColor" strokeWidth="1.5"/></svg>
                        {faculty.contacts.phone}
                      </a>
                    )}
                    {faculty.contacts?.address && (
                      <div className="contact">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 21s7-5.686 7-11a7 7 0 1 0-14 0c0 5.314 7 11 7 11Z" stroke="currentColor" strokeWidth="1.5"/><circle cx="12" cy="10" r="3" stroke="currentColor" strokeWidth="1.5"/></svg>
                        {faculty.contacts.address}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {tab === 'udruge' && (
                <div className="assoc-grid">
                  {associations.length === 0 ? (
                    <div className="empty">Nema pridruženih udruga za ovaj fakultet.</div>
                  ) : (
                    associations.map((a) => (
                      <button key={a.id} className="assoc-card" onClick={() => navigate(`/udruge/${a.slug}`)}>
                        <div className="assoc-head">
                          <div className="assoc-logo" style={{ background: a.logoBg || '#e2e8f0' }}>
                            {(a.logoText || (a.name?.split(' ').map(w => w[0]).slice(0,3).join('').toUpperCase()))}
                          </div>
                          {a.faculty && <span className="assoc-badge">{a.faculty}</span>}
                        </div>
                        <div className="assoc-title">{a.name}</div>
                        {a.shortDescription && <div className="assoc-desc">{a.shortDescription}</div>}
                      </button>
                    ))
                  )}
                </div>
              )}
            </section>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}
