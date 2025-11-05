import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import '../css/FacultiesPage.css';

const FacultiesPage = () => {
   const facultiesGridRef = useRef<HTMLDivElement>(null);
   const { isAuthenticated } = useAuth();
   const navigate = useNavigate();
   const faculties = [
      {
         id: 1,
         name: 'Fakultet elektrotehnike i računarstva',
         abbreviation: 'FER',
         description: 'Najveći fakultet u području elektrotehnike i računarstva u Hrvatskoj',
         programs: ['Računarstvo', 'Elektrotehnika', 'Automatika'],
         location: 'Zagreb',
         students: '4000+'
      },
      {
         id: 2,
         name: 'Ekonomski fakultet',
         abbreviation: 'EFZG',
         description: 'Vodeći ekonomski fakultet s tradicijom od 1925. godine',
         programs: ['Ekonomija', 'Poslovna ekonomija', 'Financije'],
         location: 'Zagreb',
         students: '6000+'
      },
      {
         id: 3,
         name: 'Fakultet organizacije i informatike',
         abbreviation: 'FOI',
         description: 'Moderan fakultet fokusiran na organizaciju i informacijske tehnologije',
         programs: ['Organizacija i informatika', 'Poslovna informatika'],
         location: 'Varaždin',
         students: '2000+'
      },
      {
         id: 4,
         name: 'Fakultet prometnih znanosti',
         abbreviation: 'FPZ',
         description: 'Fakultet specijaliziran za promet, logistiku i transport',
         programs: ['Promet', 'Logistika', 'Transport'],
         location: 'Zagreb',
         students: '1500+'
      },
      {
         id: 5,
         name: 'Pravni fakultet',
         abbreviation: 'PRAVNI',
         description: 'Jedan od najstarijih fakulteta s bogatom pravnom tradicijom',
         programs: ['Pravo', 'Pravosudje'],
         location: 'Zagreb',
         students: '5000+'
      },
      {
         id: 6,
         name: 'Fakultet strojarstva i brodogradnje',
         abbreviation: 'FSB',
         description: 'Vodeći fakultet u području strojarstva i brodogradnje',
         programs: ['Strojarstvo', 'Brodogradnja', 'Zrakoplovstvo'],
         location: 'Zagreb',
         students: '3000+'
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

      if (facultiesGridRef.current) {
         const cards = facultiesGridRef.current.querySelectorAll('.faculty-card');
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
      <div className="faculties-page">
         <Header />
         <main className="faculties-main">
            <section className="faculties-hero">
               <div className="faculties-hero-container fade-in">
                  <h1 className="faculties-hero-title slide-up">Fakulteti Sveučilišta u Zagrebu</h1>
                  <p className="faculties-hero-subtitle slide-up" style={{ animationDelay: '0.1s' }}>
                     Istraži sve fakultete i studijske programe dostupne na Sveučilištu u Zagrebu
                  </p>
                  <div className="search-wrapper slide-up" style={{ animationDelay: '0.2s' }}>
                     <input
                        type="text"
                        placeholder="Pretraži fakultete..."
                        className="faculties-search-input"
                     />
                     <button className="faculties-search-btn">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                           <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM18 18l-4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                     </button>
                  </div>
               </div>
            </section>

            <section className="faculties-list">
               <div className="faculties-container">
                  <div className="faculties-grid" ref={facultiesGridRef}>
                     {faculties.map(faculty => (
                        <div key={faculty.id} className="faculty-card">
                           <div className="faculty-header">
                              <div className="faculty-logo">
                                 {faculty.abbreviation}
                              </div>
                              <div className="faculty-info">
                                 <h3 className="faculty-name">{faculty.name}</h3>
                                 <p className="faculty-location">
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                       <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                                       <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                                    </svg>
                                    {faculty.location}
                                 </p>
                              </div>
                           </div>
                           <p className="faculty-description">{faculty.description}</p>
                           <div className="faculty-programs">
                              <h4 className="faculty-programs-title">Studijski programi:</h4>
                              <div className="faculty-programs-list">
                                 {faculty.programs.map((program, idx) => (
                                    <span key={idx} className="faculty-program-tag">{program}</span>
                                 ))}
                              </div>
                           </div>
                           <div className="faculty-footer">
                              <div className="faculty-stats">
                                 <span className="faculty-students">{faculty.students} studenata</span>
                              </div>
                              <div className="faculty-actions">
                                 <button className="faculty-btn">Saznaj više</button>
                                 {isAuthenticated && (
                                    <button 
                                       className="faculty-btn-secondary"
                                       onClick={() => {
                                          // TODO: Implementiraj slanje upita fakultetu
                                          alert('Funkcija slanja upita će biti implementirana');
                                       }}
                                    >
                                       Pošalji upit
                                    </button>
                                 )}
                              </div>
                           </div>
                        </div>
                     ))}
                  </div>
               </div>
            </section>
         </main>
         <Footer />
      </div>
   );
};

export default FacultiesPage;

