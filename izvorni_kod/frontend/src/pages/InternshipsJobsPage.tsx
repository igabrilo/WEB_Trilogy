import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Job } from '../services/api';
import Header from '../components/Header';
import FeaturedJobs from '../components/FeaturedJobs';
import Footer from '../components/Footer';
import '../css/InternshipsJobsPage.css';

const InternshipsJobsPage = () => {
   const internshipsGridRef = useRef<HTMLDivElement>(null);
   const { isAuthenticated } = useAuth();
   const navigate = useNavigate();
   const [internships, setInternships] = useState<Job[]>([]);
   const [loading, setLoading] = useState(true);
   const [activeFilter, setActiveFilter] = useState<string>('all');

   useEffect(() => {
      const loadInternships = async () => {
         setLoading(true);
         try {
            const typeFilter = activeFilter === 'all' ? undefined :
               activeFilter === 'prakse' ? 'internship' :
                  activeFilter === 'poslovi' ? 'job' :
                     activeFilter === 'djelomicno' ? 'part-time' :
                        activeFilter === 'udaljeno' ? 'remote' : undefined;

            const res = await apiService.getJobs({ type: typeFilter });
            setInternships(res.items || []);
         } catch (error) {
            console.error('Error loading internships:', error);
         } finally {
            setLoading(false);
         }
      };
      loadInternships();
   }, [activeFilter]);

   useEffect(() => {
      const observerOptions = {
         threshold: 0.1,
         rootMargin: '0px 0px -50px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
         entries.forEach((entry) => {
            if (entry.isIntersecting) {
               entry.target.classList.add('animate-in');
            }
         });
      }, observerOptions);

      if (internshipsGridRef.current) {
         const cards = internshipsGridRef.current.querySelectorAll('.internship-card');
         cards.forEach((card, index) => {
            (card as HTMLElement).style.animationDelay = `${index * 0.1}s`;
            observer.observe(card);
         });
      }

      return () => {
         observer.disconnect();
      };
   }, [internships]);

   return (
      <div className="internships-jobs-page">
         <Header />
         <main className="internships-jobs-main">
            <section className="internships-jobs-hero">
               <div className="internships-jobs-hero-container fade-in">
                  <h1 className="internships-jobs-hero-title slide-up">Prakse i Poslovi</h1>
                  <p className="internships-jobs-hero-subtitle slide-up" style={{ animationDelay: '0.1s' }}>
                     Pronađi savršenu priliku za praksu ili posao koji će ti pomoći u karijeri
                  </p>
                  <div className="filter-tabs slide-up" style={{ animationDelay: '0.2s' }}>
                     <button
                        className={`filter-tab ${activeFilter === 'all' ? 'active' : ''}`}
                        onClick={() => setActiveFilter('all')}
                     >
                        Sve
                     </button>
                     <button
                        className={`filter-tab ${activeFilter === 'prakse' ? 'active' : ''}`}
                        onClick={() => setActiveFilter('prakse')}
                     >
                        Prakse
                     </button>
                     <button
                        className={`filter-tab ${activeFilter === 'poslovi' ? 'active' : ''}`}
                        onClick={() => setActiveFilter('poslovi')}
                     >
                        Poslovi
                     </button>
                     <button
                        className={`filter-tab ${activeFilter === 'djelomicno' ? 'active' : ''}`}
                        onClick={() => setActiveFilter('djelomicno')}
                     >
                        Djelomično radno vrijeme
                     </button>
                     <button
                        className={`filter-tab ${activeFilter === 'udaljeno' ? 'active' : ''}`}
                        onClick={() => setActiveFilter('udaljeno')}
                     >
                        Udaljeno
                     </button>
                  </div>
               </div>
            </section>

            <section className="internships-section">
               <div className="internships-container">
                  <h2 className="section-title slide-up">
                     {activeFilter === 'all' ? 'Dostupne prakse i poslovi' :
                        activeFilter === 'prakse' ? 'Dostupne prakse' :
                           activeFilter === 'poslovi' ? 'Dostupni poslovi' :
                              activeFilter === 'djelomicno' ? 'Djelomično radno vrijeme' :
                                 'Udaljeno'}
                  </h2>
                  {loading ? (
                     <div style={{ padding: '2rem', textAlign: 'center' }}>Učitavanje...</div>
                  ) : internships.length === 0 ? (
                     <div style={{ padding: '2rem', textAlign: 'center' }}>
                        Nema dostupnih {activeFilter === 'all' ? 'praksi i poslova' : activeFilter === 'prakse' ? 'praksi' : 'poslova'}.
                     </div>
                  ) : (
                     <div className="internships-grid" ref={internshipsGridRef}>
                        {internships.map(internship => {
                           const typeLabel = internship.type === 'internship' ? 'Praksa' :
                              internship.type === 'job' ? 'Posao' :
                                 internship.type === 'part-time' ? 'Djelomično radno vrijeme' :
                                    internship.type === 'remote' ? 'Udaljeno' : internship.type;

                           return (
                              <div key={internship.id} className="internship-card">
                                 <div className="internship-header">
                                    <div className="internship-type-badge">{typeLabel}</div>
                                    {internship.salary && (
                                       <span className="internship-paid">Plaćeno</span>
                                    )}
                                 </div>
                                 <h3 className="internship-title">{internship.title}</h3>
                                 {internship.company && <p className="internship-company">{internship.company}</p>}
                                 <div className="internship-details">
                                    {internship.location && (
                                       <div className="internship-detail">
                                          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                             <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                                             <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                                          </svg>
                                          <span>{internship.location}</span>
                                       </div>
                                    )}
                                    {internship.createdAt && (
                                       <div className="internship-detail">
                                          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                             <path d="M2 4h12M2 8h12M2 12h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                          </svg>
                                          <span>{new Date(internship.createdAt).toLocaleDateString('hr-HR')}</span>
                                       </div>
                                    )}
                                 </div>
                                 {internship.salary && (
                                    <div style={{ marginTop: '8px', fontWeight: 600, color: '#059669' }}>
                                       {internship.salary}
                                    </div>
                                 )}
                                 <button
                                    className="internship-apply-btn"
                                    onClick={() => {
                                       if (isAuthenticated) {
                                          navigate(`/prakse-i-poslovi/${internship.id}`);
                                       } else {
                                          navigate('/prijava');
                                       }
                                    }}
                                 >
                                    {isAuthenticated ? 'Prijavi se' : 'Prijavi se (zahtijeva prijavu)'}
                                 </button>
                              </div>
                           );
                        })}
                     </div>
                  )}
               </div>
            </section>

            <FeaturedJobs />
         </main>
         <Footer />
      </div>
   );
};

export default InternshipsJobsPage;

