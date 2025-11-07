import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Faculty } from '../services/api';
import Header from '../components/Header';
import Footer from '../components/Footer';
import '../css/FacultiesPage.css';

const FacultiesPage = () => {
   const facultiesGridRef = useRef<HTMLDivElement>(null);
   const { isAuthenticated, user } = useAuth();
   const navigate = useNavigate();
   const [faculties, setFaculties] = useState<Faculty[]>([]);
   const [loading, setLoading] = useState(true);
   const [searchQuery, setSearchQuery] = useState('');
   const [favorites, setFavorites] = useState<Set<string>>(new Set());
   const [favoritesLoading, setFavoritesLoading] = useState<Set<string>>(new Set());

   useEffect(() => {
      const loadFaculties = async () => {
         setLoading(true);
         try {
            const res = await apiService.getFaculties({ q: searchQuery });
            setFaculties(res.items || []);
         } catch (error) {
            console.error('Error loading faculties:', error);
         } finally {
            setLoading(false);
         }
      };
      loadFaculties();
   }, [searchQuery]);

   // Load favorites for ucenik and student
   useEffect(() => {
      const loadFavorites = async () => {
         if (isAuthenticated && (user?.role === 'ucenik' || user?.role === 'student')) {
            try {
               const res = await apiService.getFavoriteFaculties();
               const favoriteSlugs = new Set(res.items.map(f => f.facultySlug));
               setFavorites(favoriteSlugs);
            } catch (error) {
               console.error('Error loading favorites:', error);
            }
         }
      };
      loadFavorites();
   }, [isAuthenticated, user?.role]);

   const handleToggleFavorite = async (facultySlug: string) => {
      if (!isAuthenticated || (user?.role !== 'ucenik' && user?.role !== 'student')) {
         navigate('/prijava');
         return;
      }

      setFavoritesLoading(prev => new Set(prev).add(facultySlug));

      try {
         if (favorites.has(facultySlug)) {
            await apiService.removeFavoriteFaculty(facultySlug);
            setFavorites(prev => {
               const newSet = new Set(prev);
               newSet.delete(facultySlug);
               return newSet;
            });
         } else {
            await apiService.addFavoriteFaculty(facultySlug);
            setFavorites(prev => new Set(prev).add(facultySlug));
         }
      } catch (error) {
         console.error('Error toggling favorite:', error);
         alert('Greška pri spremanju omiljenog fakulteta');
      } finally {
         setFavoritesLoading(prev => {
            const newSet = new Set(prev);
            newSet.delete(facultySlug);
            return newSet;
         });
      }
   };

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
   }, [faculties]);

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
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyDown={(e) => {
                           if (e.key === 'Enter') {
                              // Search is triggered automatically via useEffect
                           }
                        }}
                     />
                     <button className="faculties-search-btn" onClick={() => {
                        // Search is triggered automatically via useEffect
                     }}>
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                           <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM18 18l-4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                     </button>
                  </div>
               </div>
            </section>

            <section className="faculties-list">
               <div className="faculties-container">
                  {loading ? (
                     <div style={{ padding: '2rem', textAlign: 'center' }}>Učitavanje fakulteta...</div>
                  ) : faculties.length === 0 ? (
                     <div style={{ padding: '2rem', textAlign: 'center' }}>
                        {searchQuery ? 'Nema rezultata za vašu pretragu.' : 'Nema dostupnih fakulteta.'}
                     </div>
                  ) : (
                     <div className="faculties-grid" ref={facultiesGridRef}>
                        {faculties.map(faculty => (
                           <div key={faculty.slug} className="faculty-card">
                              <div className="faculty-header">
                                 <div className="faculty-logo">
                                    {faculty.abbreviation || faculty.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase()}
                                 </div>
                                 <div className="faculty-info">
                                    <h3 className="faculty-name">{faculty.name}</h3>
                                    {faculty.contacts?.address && (
                                       <p className="faculty-location">
                                          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                             <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                                             <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                                          </svg>
                                          {faculty.contacts.address.split(',')[0]}
                                       </p>
                                    )}
                                 </div>
                                 {(user?.role === 'ucenik' || user?.role === 'student') && (
                                    <button
                                       className="favorite-btn"
                                       onClick={() => handleToggleFavorite(faculty.slug)}
                                       disabled={favoritesLoading.has(faculty.slug)}
                                       style={{
                                          background: 'transparent',
                                          border: 'none',
                                          cursor: 'pointer',
                                          padding: '0.5rem',
                                          display: 'flex',
                                          alignItems: 'center',
                                          justifyContent: 'center',
                                          color: favorites.has(faculty.slug) ? '#fbbf24' : '#94a3b8',
                                          transition: 'color 0.2s'
                                       }}
                                       title={favorites.has(faculty.slug) ? 'Ukloni iz omiljenih' : 'Dodaj u omiljene'}
                                    >
                                       <svg width="24" height="24" viewBox="0 0 24 24" fill={favorites.has(faculty.slug) ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2">
                                          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                       </svg>
                                    </button>
                                 )}
                              </div>
                              {faculty.contacts?.website && (
                                 <p className="faculty-description" style={{ fontSize: '0.875rem', color: '#64748b' }}>
                                    {faculty.contacts.website.replace(/^https?:\/\//, '')}
                                 </p>
                              )}
                              <div className="faculty-footer">
                                 <div className="faculty-actions">
                                    <button
                                       className="faculty-btn"
                                       onClick={() => navigate(`/fakulteti/${faculty.slug}`)}
                                    >
                                       Saznaj više
                                    </button>
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
                  )}
               </div>
            </section>
         </main>
         <Footer />
      </div>
   );
};

export default FacultiesPage;

