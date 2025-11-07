import { useEffect, useMemo, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type Association, type Faculty } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
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
  const location = useLocation();
  const { user } = useAuth();
  const [faculty, setFaculty] = useState<Faculty | null>(null);
  const [loading, setLoading] = useState(true);
  
  // Get initial tab from URL query parameter
  const getTabFromUrl = () => {
    const searchParams = new URLSearchParams(location.search);
    const tabParam = searchParams.get('tab') as 'pregled' | 'udruge' | 'upit' | null;
    return (tabParam && ['pregled', 'udruge', 'upit'].includes(tabParam)) ? tabParam : 'pregled';
  };
  
  const [tab, setTab] = useState<'pregled' | 'udruge' | 'upit'>(getTabFromUrl());
  const [associations, setAssociations] = useState<Association[]>([]);
  const [inquiryForm, setInquiryForm] = useState({
    senderName: '',
    senderEmail: '',
    subject: '',
    message: '',
  });
  const [inquiryLoading, setInquiryLoading] = useState(false);
  const [inquirySuccess, setInquirySuccess] = useState(false);

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

  // Update tab when URL query parameter changes
  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const tabParam = searchParams.get('tab') as 'pregled' | 'udruge' | 'upit' | null;
    if (tabParam && ['pregled', 'udruge', 'upit'].includes(tabParam)) {
      setTab(tabParam);
    } else if (!tabParam) {
      setTab('pregled');
    }
  }, [location.search]);

  useEffect(() => {
    const loadAssociations = async () => {
      if (!faculty?.abbreviation) return;
      const res = await apiService.getAssociations({ faculty: faculty.abbreviation });
      setAssociations(res.items || []);
    };
    if (tab === 'udruge') loadAssociations();
  }, [tab, faculty?.abbreviation]);

  useEffect(() => {
    // Pre-fill form if user is logged in
    if (user && !inquiryForm.senderName && !inquiryForm.senderEmail) {
      setInquiryForm(prev => ({
        ...prev,
        senderName: `${user.firstName || ''} ${user.lastName || ''}`.trim() || user.username || '',
        senderEmail: user.email || '',
      }));
    }
  }, [user]);

  const handleSendInquiry = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!faculty) return;

    setInquiryLoading(true);
    setInquirySuccess(false);
    try {
      await apiService.sendFacultyInquiry({
        facultySlug: faculty.slug,
        ...inquiryForm,
      });
      setInquirySuccess(true);
      setInquiryForm({ senderName: '', senderEmail: '', subject: '', message: '' });
      setTimeout(() => {
        setInquirySuccess(false);
      }, 5000);
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Greška pri slanju upita');
    } finally {
      setInquiryLoading(false);
    }
  };

  const coverStyle = useMemo(() => ({ background: colorFromSlug(slug) }), [slug]);
  const logoText = faculty?.abbreviation || faculty?.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase();

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

            <section className="container" style={{ padding: '1.5rem 1rem', maxWidth: '1200px', margin: '0 auto' }}>
              <nav className="faculty-tabs">
                <button className={`tab ${tab === 'pregled' ? 'active' : ''}`} onClick={() => {
                  setTab('pregled');
                  navigate(`/fakulteti/${slug}`, { replace: true });
                }}>Pregled</button>
                <button className={`tab ${tab === 'udruge' ? 'active' : ''}`} onClick={() => {
                  setTab('udruge');
                  navigate(`/fakulteti/${slug}`, { replace: true });
                }}>Udruge</button>
                <button className={`tab ${tab === 'upit' ? 'active' : ''}`} onClick={() => {
                  setTab('upit');
                  navigate(`/fakulteti/${slug}?tab=upit`, { replace: true });
                }}>Pošaljite upit</button>
              </nav>

              {tab === 'pregled' && (
                <div className="faculty-about">
                  <h2 style={{ margin: '0 0 1rem', fontSize: '1.25rem', fontWeight: 700, color: '#0f172a' }}>Kontakt informacije</h2>
                  <div className="contacts">
                    {faculty.contacts?.website && (
                      <a className="contact" href={faculty.contacts.website} target="_blank" rel="noreferrer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M3 12a9 9 0 1 0 18 0A9 9 0 0 0 3 12Zm5 0a4 4 0 1 0 8 0 4 4 0 0 0-8 0Z" stroke="currentColor" strokeWidth="1.5" /></svg>
                        <span>{faculty.contacts.website.replace(/^https?:\/\//, '')}</span>
                      </a>
                    )}
                    {faculty.contacts?.email && (
                      <a className="contact" href={`mailto:${faculty.contacts.email}`}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M4 6h16v12H4z" stroke="currentColor" strokeWidth="1.5" /><path d="m4 6 8 6 8-6" stroke="currentColor" strokeWidth="1.5" /></svg>
                        <span>{faculty.contacts.email}</span>
                      </a>
                    )}
                    {faculty.contacts?.phone && (
                      <a className="contact" href={`tel:${faculty.contacts.phone.replace(/\s+/g, '')}`}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M6 2h4l2 5-3 2a11 11 0 0 0 6 6l2-3 5 2v4a3 3 0 0 1-3 3c-10 0-18-8-18-18a3 3 0 0 1 3-3Z" stroke="currentColor" strokeWidth="1.5" /></svg>
                        <span>{faculty.contacts.phone}</span>
                      </a>
                    )}
                    {faculty.contacts?.address && (
                      <div className="contact">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 21s7-5.686 7-11a7 7 0 1 0-14 0c0 5.314 7 11 7 11Z" stroke="currentColor" strokeWidth="1.5" /><circle cx="12" cy="10" r="3" stroke="currentColor" strokeWidth="1.5" /></svg>
                        <span>{faculty.contacts.address}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {tab === 'udruge' && (
                <div>
                  <h2 style={{ margin: '0 0 1rem', fontSize: '1.25rem', fontWeight: 700, color: '#0f172a' }}>
                    Studentske udruge ({associations.length})
                  </h2>
                  <div className="assoc-grid">
                    {associations.length === 0 ? (
                      <div className="empty">Nema pridruženih udruga za ovaj fakultet.</div>
                    ) : (
                      associations.map((a) => (
                        <button key={a.id} className="assoc-card" onClick={() => navigate(`/udruge/${a.slug}`)}>
                          <div className="assoc-head">
                            <div className="assoc-logo" style={{ background: a.logoBg || '#e2e8f0' }}>
                              {(a.logoText || (a.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase()))}
                            </div>
                            {a.faculty && <span className="assoc-badge">{a.faculty}</span>}
                          </div>
                          <div className="assoc-title">{a.name}</div>
                          {a.shortDescription && <div className="assoc-desc">{a.shortDescription}</div>}
                        </button>
                      ))
                    )}
                  </div>
                </div>
              )}

              {tab === 'upit' && (
                <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                  <h2 style={{ margin: '0 0 1.5rem', fontSize: '1.25rem', fontWeight: 700, color: '#0f172a' }}>
                    Pošaljite upit fakultetu
                  </h2>
                  {inquirySuccess && (
                    <div style={{ padding: '1rem', marginBottom: '1.5rem', background: '#10b981', color: 'white', borderRadius: '8px' }}>
                      Upit je uspješno poslan! Fakultet će vas kontaktirati ubrzo.
                    </div>
                  )}
                  <form onSubmit={handleSendInquiry} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div>
                      <label htmlFor="senderName" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#334155' }}>
                        Ime i prezime *
                      </label>
                      <input
                        type="text"
                        id="senderName"
                        required
                        value={inquiryForm.senderName}
                        onChange={(e) => setInquiryForm(prev => ({ ...prev, senderName: e.target.value }))}
                        style={{ width: '100%', padding: '0.75rem', border: '1px solid #cbd5e1', borderRadius: '8px', fontSize: '1rem' }}
                      />
                    </div>
                    <div>
                      <label htmlFor="senderEmail" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#334155' }}>
                        Email adresa *
                      </label>
                      <input
                        type="email"
                        id="senderEmail"
                        required
                        value={inquiryForm.senderEmail}
                        onChange={(e) => setInquiryForm(prev => ({ ...prev, senderEmail: e.target.value }))}
                        style={{ width: '100%', padding: '0.75rem', border: '1px solid #cbd5e1', borderRadius: '8px', fontSize: '1rem' }}
                      />
                    </div>
                    <div>
                      <label htmlFor="subject" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#334155' }}>
                        Predmet *
                      </label>
                      <input
                        type="text"
                        id="subject"
                        required
                        value={inquiryForm.subject}
                        onChange={(e) => setInquiryForm(prev => ({ ...prev, subject: e.target.value }))}
                        placeholder="npr. Pitanje o studijskim programima"
                        style={{ width: '100%', padding: '0.75rem', border: '1px solid #cbd5e1', borderRadius: '8px', fontSize: '1rem' }}
                      />
                    </div>
                    <div>
                      <label htmlFor="message" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#334155' }}>
                        Poruka *
                      </label>
                      <textarea
                        id="message"
                        required
                        rows={6}
                        value={inquiryForm.message}
                        onChange={(e) => setInquiryForm(prev => ({ ...prev, message: e.target.value }))}
                        placeholder="Vaša poruka..."
                        style={{ width: '100%', padding: '0.75rem', border: '1px solid #cbd5e1', borderRadius: '8px', fontSize: '1rem', fontFamily: 'inherit', resize: 'vertical' }}
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={inquiryLoading}
                      style={{
                        padding: '0.75rem 1.5rem',
                        background: inquiryLoading ? '#94a3b8' : '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        fontSize: '1rem',
                        fontWeight: 500,
                        cursor: inquiryLoading ? 'not-allowed' : 'pointer',
                        alignSelf: 'flex-start',
                      }}
                    >
                      {inquiryLoading ? 'Slanje...' : 'Pošalji upit'}
                    </button>
                  </form>
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
