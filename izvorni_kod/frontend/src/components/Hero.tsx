import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService, type Association, type Faculty } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import '../css/Hero.css';

const Hero = () => {
   const profileCardsRef = useRef<HTMLDivElement>(null);
   const heroSearchRef = useRef<HTMLElement>(null);
   const [query, setQuery] = useState('');
   const [assocResults, setAssocResults] = useState<Association[]>([]);
   const [facultyResults, setFacultyResults] = useState<Faculty[]>([]);
   const [loading, setLoading] = useState(false);
   const [open, setOpen] = useState(false); // legacy state from dropdown; kept for focus behavior
   const suggestBoxRef = useRef<HTMLDivElement>(null);
   const navigate = useNavigate();
   const { user } = useAuth();

   useEffect(() => {
      const observerOptions = {
         threshold: 0.1,
         rootMargin: '0px 0px -100px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
         entries.forEach((entry) => {
            if (entry.isIntersecting) {
               entry.target.classList.add('animate-in');
            }
         });
      }, observerOptions);

      if (profileCardsRef.current) {
         const cards = profileCardsRef.current.querySelectorAll('.profile-card');
         cards.forEach((card, index) => {
            (card as HTMLElement).style.animationDelay = `${index * 0.1}s`;
            observer.observe(card);
         });
      }

      const handleScroll = () => {
         if (heroSearchRef.current) {
            const scrolled = window.scrollY;
            const rate = scrolled * 0.3;
            heroSearchRef.current.style.transform = `translateY(${rate}px)`;
         }
      };

      window.addEventListener('scroll', handleScroll, { passive: true });

      return () => {
         observer.disconnect();
         window.removeEventListener('scroll', handleScroll);
      };
   }, []);

   // Fetch suggestions with debounce when query changes
   useEffect(() => {
      const q = query.trim();
      // Only search if query is at least 2 characters
      if (!q || q.length < 2) {
         setAssocResults([]);
         setFacultyResults([]);
         setOpen(false);
         return;
      }
      setLoading(true);
      const t = setTimeout(async () => {
         try {
            const res = await apiService.searchAll({ q, faculty: user?.faculty || undefined });
            setAssocResults(res.results.associations || []);
            setFacultyResults(res.results.faculties || []);
            setOpen(true);
         } catch (e) {
            console.error('Search error:', e);
            setAssocResults([]);
            setFacultyResults([]);
            setOpen(false);
         } finally {
            setLoading(false);
         }
      }, 300);
      return () => clearTimeout(t);
   }, [query, user?.faculty]);

   // Close suggestions on outside click
   useEffect(() => {
      const onClick = (e: MouseEvent) => {
         if (!suggestBoxRef.current) return;
         if (!suggestBoxRef.current.contains(e.target as Node)) {
            setOpen(false);
         }
      };
      document.addEventListener('click', onClick);
      return () => document.removeEventListener('click', onClick);
   }, []);

   return (
      <>
         <section className="hero-search" ref={heroSearchRef}>
            <div className="hero-search-container fade-in">
               <h1 className="hero-search-title slide-up">Tvoja karijera počinje ovdje</h1>
               <p className="hero-search-subtitle slide-up" style={{ animationDelay: '0.1s' }}>
                  Povezujemo studente, alumni, poslodavce i fakultete Sveučilišta u Zagrebu.
                  Pronađi praksu, posao ili savršen fakultet za sebe.
               </p>
               <div className="search-wrapper slide-up" style={{ animationDelay: '0.2s' }}>
                  <div className="search-box" ref={suggestBoxRef} onKeyDown={(e) => { if ((e as unknown as KeyboardEvent).key === 'Enter') navigate(`/pretraga?q=${encodeURIComponent(query)}`); }}>
                     <input
                        type="text"
                        placeholder="Pretraži fakultete, udruge, praksu, posao..."
                        className="search-input-main"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                                    onFocus={() => { if (assocResults.length + facultyResults.length > 0) setOpen(true); }}
                     />
                     <button className="search-category-btn" onClick={() => navigate(`/pretraga?q=${encodeURIComponent(query)}`)}>Sve kategorije</button>
                     <button className="search-submit-btn" onClick={() => navigate(`/pretraga?q=${encodeURIComponent(query)}`)}>
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                           <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM18 18l-4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        Pretraži
                     </button>
                     {/* Inline live results rendered below, not dropdown */}
                  </div>
                  <div className="quick-filters">
                     <button className="filter-btn" onClick={() => navigate(`/pretraga?q=${encodeURIComponent('praksa')}`)}>Praksa</button>
                     <button className="filter-btn" onClick={() => navigate(`/pretraga?q=${encodeURIComponent('student')}`)}>Student</button>
                     <button className="filter-btn" onClick={() => navigate(`/pretraga?q=${encodeURIComponent('alumni')}`)}>Alumni</button>
                     <button className="filter-btn" onClick={() => navigate(`/pretraga?q=${encodeURIComponent('part-time')}`)}>Part-time</button>
                     <button className="filter-btn" onClick={() => navigate(`/pretraga?q=${encodeURIComponent('remote')}`)}>Remote</button>
                  </div>
               </div>
               {/* Live results section under search bar */}
               {(query.trim().length >= 2) && (
                  <div className="live-results">
                     {loading && <div className="live-status">Pretraživanje...</div>}
                     {!loading && (assocResults.length + facultyResults.length === 0) && (
                        <div className="live-status">Nema rezultata</div>
                     )}
                     {!loading && assocResults.length > 0 && (
                        <div className="live-section">
                           <div className="live-section-header">Udruge</div>
                           <div className="live-grid">
                              {assocResults.map((a) => (
                                 <button key={a.id} className="live-card" onClick={() => navigate(`/udruge/${a.slug}`)}>
                                    <div className="live-card-head">
                                       <div className="live-logo" style={{ background: a.logoBg || '#e2e8f0' }}>
                                          {(a.logoText || (a.name?.split(' ').map(w => w[0]).slice(0,3).join('').toUpperCase()))}
                                       </div>
                                       {a.faculty && <span className="live-badge">{a.faculty}</span>}
                                    </div>
                                    <div className="live-title">{a.name}</div>
                                    {a.shortDescription && <div className="live-desc">{a.shortDescription}</div>}
                                 </button>
                              ))}
                           </div>
                        </div>
                     )}
                     {!loading && facultyResults.length > 0 && (
                        <div className="live-section">
                           <div className="live-section-header">Fakulteti i akademije</div>
                           <div className="live-grid">
                               {facultyResults.map((f) => (
                                <div key={f.slug} className="live-card" onClick={() => navigate(`/fakulteti/${f.slug}`)} role="button" tabIndex={0} onKeyDown={(e) => { if (e.key === 'Enter') navigate(`/fakulteti/${f.slug}`); }}>
                                    <div className="live-card-head">
                                       <div className="live-logo" style={{ background: '#1e70bf' }}>
                                          {(f.abbreviation || f.name?.split(' ').map(w => w[0]).slice(0,3).join('').toUpperCase())}
                                       </div>
                                       <span className="live-badge">{f.type === 'academy' ? 'Akademija' : 'Fakultet'}</span>
                                    </div>
                                    <div className="live-title">{f.name}</div>
                                    {f.contacts && (
                                       <div className="live-contacts">
                                                                {f.contacts.website && (
                                                                   <a className="contact-link" href={f.contacts.website} target="_blank" rel="noreferrer" onClick={(e) => e.stopPropagation()}>
                                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M3 12a9 9 0 1 0 18 0A9 9 0 0 0 3 12Zm5 0a4 4 0 1 0 8 0 4 4 0 0 0-8 0Z" stroke="currentColor" strokeWidth="1.5"/></svg>
                                                Web
                                             </a>
                                          )}
                                          {f.contacts.email && (
                                             <span className="contact-item">
                                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M4 6h16v12H4z" stroke="currentColor" strokeWidth="1.5"/><path d="m4 6 8 6 8-6" stroke="currentColor" strokeWidth="1.5"/></svg>
                                                {f.contacts.email}
                                             </span>
                                          )}
                                          {f.contacts.phone && (
                                             <span className="contact-item">
                                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M6 2h4l2 5-3 2a11 11 0 0 0 6 6l2-3 5 2v4a3 3 0 0 1-3 3c-10 0-18-8-18-18a3 3 0 0 1 3-3Z" stroke="currentColor" strokeWidth="1.5"/></svg>
                                                {f.contacts.phone}
                                             </span>
                                          )}
                                          {f.contacts.address && (
                                             <span className="contact-item">
                                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 21s7-5.686 7-11a7 7 0 1 0-14 0c0 5.314 7 11 7 11Z" stroke="currentColor" strokeWidth="1.5"/><circle cx="12" cy="10" r="3" stroke="currentColor" strokeWidth="1.5"/></svg>
                                                {f.contacts.address}
                                             </span>
                                          )}
                                       </div>
                                    )}
                                </div>
                              ))}
                           </div>
                        </div>
                     )}
                  </div>
               )}
            </div>
         </section>

         <section className="profile-selection-section">
            <div className="profile-selection-container">
               <h2 className="profile-section-title">Odaberi svoj profil</h2>
               <p className="profile-section-subtitle">Prilagođeno iskustvo za svaku vrstu korisnika</p>

                  <div className="profile-grid" ref={profileCardsRef}>
                  <div className="profile-card" role="button" tabIndex={0} onClick={() => navigate('/profil/ucenik')} onKeyDown={(e) => { if (e.key==='Enter') navigate('/profil/ucenik'); }}>
                     <div className="profile-icon blue-icon">
                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                           <path d="M24 24c4.4 0 8-3.6 8-8s-3.6-8-8-8-8 3.6-8 8 3.6 8 8 8zm0 4c-5.3 0-16 2.7-16 8v4h32v-4c0-5.3-10.7-8-16-8z" fill="currentColor" />
                           <path d="M24 10l-8 3.2v4l8 3.2 8-3.2v-4L24 10z" stroke="currentColor" strokeWidth="2" fill="none" />
                        </svg>
                     </div>
                     <h3 className="profile-card-title">Učenik</h3>
                     <p className="profile-card-subtitle">Učenik srednje škole</p>
                     <ul className="profile-features">
                        <li>Pretraga fakulteta za upis</li>
                        <li>Prilike za učenički servis</li>
                        <li>Savjeti za studiranje</li>
                        <li>Scholarship favoriti</li>
                     </ul>
                  </div>

                  <div className="profile-card" role="button" tabIndex={0} onClick={() => navigate('/profil/student')} onKeyDown={(e) => { if (e.key==='Enter') navigate('/profil/student'); }}>
                     <div className="profile-icon blue-icon">
                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                           <circle cx="24" cy="16" r="6" stroke="currentColor" strokeWidth="2.5" />
                           <path d="M12 36c0-6.6 5.4-12 12-12s12 5.4 12 12" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
                           <path d="M24 8l-10 4v5l10 4 10-4v-5l-10-4z" stroke="currentColor" strokeWidth="2" fill="none" />
                        </svg>
                     </div>
                     <h3 className="profile-card-title">Student</h3>
                     <p className="profile-card-subtitle">Trenutni student uniZG-a</p>
                     <ul className="profile-features">
                        <li>Predefinirane prakse i poslovi</li>
                        <li>Erasmus projekti grupe</li>
                        <li>Studentske udruge</li>
                        <li>Profesionalni profili</li>
                     </ul>
                  </div>

                  <div className="profile-card" role="button" tabIndex={0} onClick={() => navigate('/profil/alumni')} onKeyDown={(e) => { if (e.key==='Enter') navigate('/profil/alumni'); }}>
                     <div className="profile-icon blue-icon">
                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                           <circle cx="24" cy="16" r="6" stroke="currentColor" strokeWidth="2.5" />
                           <path d="M12 36c0-6.6 5.4-12 12-12s12 5.4 12 12" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
                           <path d="M32 12l4 4-4 4m-16-8l-4 4 4 4" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                     </div>
                     <h3 className="profile-card-title">Alumnus</h3>
                     <p className="profile-card-subtitle">Alumnus alumni i UniZG-a</p>
                     <ul className="profile-features">
                        <li>Pronađi poslove i projekte</li>
                        <li>Alumni mreža</li>
                        <li>Mentoriranje studenta</li>
                        <li>Dogadjanja i networking</li>
                     </ul>
                  </div>

                  <div className="profile-card" role="button" tabIndex={0} onClick={() => navigate('/profil/poslodavac')} onKeyDown={(e) => { if (e.key==='Enter') navigate('/profil/poslodavac'); }}>
                     <div className="profile-icon blue-icon">
                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                           <rect x="8" y="14" width="32" height="24" rx="2" stroke="currentColor" strokeWidth="2.5" />
                           <path d="M16 14V10c0-1.1.9-2 2-2h12c1.1 0 2 .9 2 2v4" stroke="currentColor" strokeWidth="2.5" />
                           <line x1="8" y1="22" x2="40" y2="22" stroke="currentColor" strokeWidth="2.5" />
                           <circle cx="24" cy="28" r="3" stroke="currentColor" strokeWidth="2" />
                        </svg>
                     </div>
                     <h3 className="profile-card-title">Poslodavac</h3>
                     <p className="profile-card-subtitle">Tvrtke i organizacije</p>
                     <ul className="profile-features">
                        <li>Objavljivanje oglasa</li>
                        <li>Pregled i filtering kandidata</li>
                        <li>Objava kompanijske slike</li>
                        <li>Djelatnost u usluzi</li>
                     </ul>
                  </div>

                  <div className="profile-card" role="button" tabIndex={0} onClick={() => navigate('/profil/fakultet')} onKeyDown={(e) => { if (e.key==='Enter') navigate('/profil/fakultet'); }}>
                     <div className="profile-icon blue-icon">
                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                           <rect x="8" y="10" width="32" height="28" rx="2" stroke="currentColor" strokeWidth="2.5" />
                           <line x1="8" y1="18" x2="40" y2="18" stroke="currentColor" strokeWidth="2.5" />
                           <path d="M16 26h16M16 32h10" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
                           <circle cx="24" cy="6" r="2" fill="currentColor" />
                        </svg>
                     </div>
                     <h3 className="profile-card-title">Fakultet</h3>
                     <p className="profile-card-subtitle">Sveučilišne institucije</p>
                     <ul className="profile-features">
                        <li>Promocija studijskih programa</li>
                        <li>Upravljanje studijskim sadržajima</li>
                        <li>Pregled i financija država</li>
                        <li>Studentska usluga</li>
                     </ul>
                  </div>
               </div>
            </div>
         </section>
      </>
   );
};

export default Hero;
