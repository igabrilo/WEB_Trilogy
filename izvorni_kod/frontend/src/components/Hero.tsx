import { useEffect, useRef } from 'react';
import '../css/Hero.css';

const Hero = () => {
   const profileCardsRef = useRef<HTMLDivElement>(null);
   const heroSearchRef = useRef<HTMLElement>(null);

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
                  <div className="search-box">
                     <input
                        type="text"
                        placeholder="Pretraži fakultete, praksu, posao..."
                        className="search-input-main"
                     />
                     <button className="search-category-btn">Sve kategorije</button>
                     <button className="search-submit-btn">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                           <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM18 18l-4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        Pretraži
                     </button>
                  </div>
                  <div className="quick-filters">
                     <button className="filter-btn">Praksa</button>
                     <button className="filter-btn">Student</button>
                     <button className="filter-btn">Alumni</button>
                     <button className="filter-btn">Part-time</button>
                     <button className="filter-btn">Remote</button>
                  </div>
               </div>
            </div>
         </section>

         <section className="profile-selection-section">
            <div className="profile-selection-container">
               <h2 className="profile-section-title">Odaberi svoj profil</h2>
               <p className="profile-section-subtitle">Prilagođeno iskustvo za svaku vrstu korisnika</p>

               <div className="profile-grid" ref={profileCardsRef}>
                  <div className="profile-card">
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

                  <div className="profile-card">
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
                        <li>Studentske usluge</li>
                        <li>Profesionalni profili</li>
                     </ul>
                  </div>

                  <div className="profile-card">
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
                        <li>Mentorstvo studente</li>
                        <li>Dogadjanja i networking</li>
                     </ul>
                  </div>

                  <div className="profile-card">
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

                  <div className="profile-card">
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
