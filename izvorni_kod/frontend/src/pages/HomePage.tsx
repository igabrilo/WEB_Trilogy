import { useEffect, useState } from 'react';
import Header from '../components/Header';
import Hero from '../components/Hero';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Association } from '../services/api';

const HomePage = () => {
   const { isAuthenticated, user } = useAuth();
   const [associations, setAssociations] = useState<Association[]>([]);

   useEffect(() => {
      const load = async () => {
         if (isAuthenticated && (user?.role === 'student' || user?.role === 'alumni' || user?.role === 'ucenik')) {
            const res = await apiService.getAssociations({ faculty: user?.faculty || undefined });
            let items = res.items;
            if (user?.interests && user.interests.length > 0) {
               const interestsLower = user.interests.map(i => i.toLowerCase());
               items = items.sort((a, b) => {
                  const at = (a.tags || []).map(t => t.toLowerCase());
                  const bt = (b.tags || []).map(t => t.toLowerCase());
                  const am = at.some(t => interestsLower.includes(t)) ? 1 : 0;
                  const bm = bt.some(t => interestsLower.includes(t)) ? 1 : 0;
                  return bm - am; // put matches first
               });
            }
            setAssociations(items.slice(0, 4));
         } else {
            setAssociations([]);
         }
      };
      load();
   }, [isAuthenticated, user?.role, user?.faculty]);

   return (
      <div className="home-page">
         <Header />
         <Hero />
         {associations.length > 0 && (
            <section className="container" style={{ padding: '2rem 1rem' }}>
               <h2 style={{ marginBottom: 12 }}>Preporučene studentske udruge {user?.faculty ? `za ${user.faculty}` : ''}</h2>
               <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '16px' }}>
                  {associations.map((a) => (
                     <a key={a.id} href={`/udruge/${a.slug}`} style={{ padding: 16, border: '1px solid #eee', borderRadius: 8, textDecoration: 'none', color: 'inherit' }}>
                        <h3 style={{ margin: '0 0 8px' }}>{a.name}</h3>
                        {a.shortDescription && <p style={{ margin: 0, color: '#555' }}>{a.shortDescription}</p>}
                     </a>
                  ))}
               </div>
            </section>
         )}
         <Footer />
      </div>
   );
};

export default HomePage;
