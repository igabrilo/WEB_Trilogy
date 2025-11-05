import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import FeaturedJobs from '../components/FeaturedJobs';
import Footer from '../components/Footer';
import '../css/InternshipsJobsPage.css';

const InternshipsJobsPage = () => {
   const internshipsGridRef = useRef<HTMLDivElement>(null);
   const { isAuthenticated } = useAuth();
   const navigate = useNavigate();
   const internships = [
      {
         id: 1,
         title: 'Ljetna praksa - Software Development',
         company: 'Tech Solutions d.o.o.',
         location: 'Zagreb, Croatia',
         duration: '3 mjeseca',
         type: 'Praksa',
         paid: true,
         posted: '5 dana'
      },
      {
         id: 2,
         title: 'Marketing Internship',
         company: 'Digital Agency',
         location: 'Remote',
         duration: '6 mjeseci',
         type: 'Praksa',
         paid: true,
         posted: '2 dana'
      },
      {
         id: 3,
         title: 'Research Assistant',
         company: 'FER Research Lab',
         location: 'Zagreb, Croatia',
         duration: '1 godina',
         type: 'Part-time',
         paid: true,
         posted: '1 tjedan'
      },
      {
         id: 4,
         title: 'UX/UI Design Internship',
         company: 'Creative Studio',
         location: 'Zagreb, Croatia',
         duration: '3 mjeseca',
         type: 'Praksa',
         paid: false,
         posted: '3 dana'
      }
   ];

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
   }, []);

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
                     <button className="filter-tab active">Sve</button>
                     <button className="filter-tab">Prakse</button>
                     <button className="filter-tab">Poslovi</button>
                     <button className="filter-tab">Part-time</button>
                     <button className="filter-tab">Remote</button>
                  </div>
               </div>
            </section>

            <section className="internships-section">
               <div className="internships-container">
                  <h2 className="section-title slide-up">Dostupne prakse</h2>
                  <div className="internships-grid" ref={internshipsGridRef}>
                     {internships.map(internship => (
                        <div key={internship.id} className="internship-card">
                           <div className="internship-header">
                              <div className="internship-type-badge">{internship.type}</div>
                              {internship.paid && (
                                 <span className="internship-paid">Plaćeno</span>
                              )}
                           </div>
                           <h3 className="internship-title">{internship.title}</h3>
                           <p className="internship-company">{internship.company}</p>
                           <div className="internship-details">
                              <div className="internship-detail">
                                 <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                                    <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                                 </svg>
                                 <span>{internship.location}</span>
                              </div>
                              <div className="internship-detail">
                                 <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <path d="M8 1v7l4 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                    <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" />
                                 </svg>
                                 <span>{internship.duration}</span>
                              </div>
                              <div className="internship-detail">
                                 <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <path d="M2 4h12M2 8h12M2 12h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                 </svg>
                                 <span>{internship.posted}</span>
                              </div>
                           </div>
                           <button 
                              className="internship-apply-btn"
                              onClick={() => {
                                 if (isAuthenticated) {
                                    // TODO: Implementiraj prijavu na praksu/posao
                                    alert('Funkcija prijave će biti implementirana');
                                 } else {
                                    navigate('/prijava');
                                 }
                              }}
                           >
                              {isAuthenticated ? 'Prijavi se' : 'Prijavi se (zahtijeva prijavu)'}
                           </button>
                        </div>
                     ))}
                  </div>
               </div>
            </section>

            <FeaturedJobs />
         </main>
         <Footer />
      </div>
   );
};

export default InternshipsJobsPage;

