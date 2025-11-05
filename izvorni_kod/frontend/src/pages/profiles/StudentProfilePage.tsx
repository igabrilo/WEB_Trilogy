import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useAuth } from '../../contexts/AuthContext';
import { apiService, type Association, type Faculty } from '../../services/api';

export default function StudentProfilePage() {
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
        setAssociations(assocRes.items.slice(0, 6));
        setFaculties(facRes.items.slice(0, 6));
      } catch {}
    };
    run();
  }, [user?.faculty]);

  return (
    <div className="student-profile-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Dobrodošao/la, {user?.firstName || 'student'}</h1>
        <p style={{ color:'#475569', marginTop: 4 }}>Sve na jednom mjestu: prakse, fakulteti, studentske organizacije i resursi.</p>

        <div style={{ display:'flex', gap:12, flexWrap:'wrap', marginTop:16 }}>
          <button className="btn-primary" onClick={() => navigate('/prakse-i-poslovi')}>Prakse i poslovi</button>
          <button className="btn-primary" onClick={() => navigate('/fakulteti')}>Fakulteti</button>
          <button className="btn-primary" onClick={() => navigate('/udruge')}>Studentske udruge</button>
          <button className="btn-secondary" onClick={() => navigate('/resursi')}>Resursi</button>
        </div>

        <section style={{ marginTop: 28 }}>
          <h2 style={{ marginBottom: 12 }}>Preporučene udruge {user?.faculty ? `za ${user.faculty}` : ''}</h2>
          {associations.length === 0 ? (
            <p>Nema preporuka trenutno.</p>
          ) : (
            <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(240px,1fr))', gap:16 }}>
              {associations.map(a => (
                <Link to={`/udruge/${a.slug}`} key={a.id} className="card" style={{ padding: 14, border:'1px solid #e2e8f0', borderRadius: 8, textDecoration:'none', color:'inherit' }}>
                  <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:6 }}>
                    <div style={{ width:36, height:36, borderRadius:8, background:a.logoBg || '#1e293b', color:'#fff', display:'grid', placeItems:'center', fontWeight:700 }}>{a.logoText || (a.name?.split(' ').map(w=>w[0]).slice(0,3).join('').toUpperCase())}</div>
                    <div style={{ fontWeight:700 }}>{a.name}</div>
                  </div>
                  {a.shortDescription && <div style={{ color:'#475569' }}>{a.shortDescription}</div>}
                </Link>
              ))}
            </div>
          )}
        </section>

        <section style={{ marginTop: 28 }}>
          <h2 style={{ marginBottom: 12 }}>Izdvojeni fakulteti</h2>
          {faculties.length === 0 ? (
            <p>Nema fakulteta za prikaz.</p>
          ) : (
            <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(240px,1fr))', gap:16 }}>
              {faculties.map(f => (
                <Link to={`/fakulteti/${f.slug}`} key={f.slug} className="card" style={{ padding: 14, border:'1px solid #e2e8f0', borderRadius: 8, textDecoration:'none', color:'inherit' }}>
                  <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                    <div style={{ width:36, height:36, borderRadius:8, background:'#1e70bf', color:'#fff', display:'grid', placeItems:'center', fontWeight:700 }}>{f.abbreviation || f.name?.split(' ').map(w=>w[0]).slice(0,3).join('').toUpperCase()}</div>
                    <div style={{ fontWeight:700 }}>{f.name}</div>
                  </div>
                  {f.contacts?.address && <div style={{ color:'#475569', marginTop:6 }}>{f.contacts.address}</div>}
                </Link>
              ))}
            </div>
          )}
        </section>
      </main>
      <Footer />
    </div>
  );
}
