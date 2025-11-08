import { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type Association, type Faculty } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function useQueryParam(name: string) {
  const { search } = useLocation();
  return new URLSearchParams(search).get(name) || '';
}

const SearchResultsPage = () => {
  const { user } = useAuth();
  const q = useQueryParam('q');
  const [loading, setLoading] = useState(true);
  const [associations, setAssociations] = useState<Association[]>([]);
  const [faculties, setFaculties] = useState<Faculty[]>([]);

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      try {
        const res = await apiService.searchAll({ q, faculty: user?.faculty || undefined });
        setAssociations(res.results.associations || []);
        setFaculties(res.results.faculties || []);
      } finally {
        setLoading(false);
      }
    };
    if (q) run();
    else {
      setAssociations([]);
      setLoading(false);
    }
  }, [q, user?.faculty]);

  return (
    <div className="search-results-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Rezultati pretrage</h1>
        <div style={{ color: '#475569', marginBottom: 16 }}>Pojam: "{q}" {user?.faculty ? `(fakultet: ${user.faculty})` : ''}</div>

        {loading ? (
          <p>Pretraživanje...</p>
        ) : (
          <>
            <h2 style={{ marginTop: 24 }}>Studentske udruge</h2>
            {associations.length === 0 ? (
              <p>Nema pronađenih udruga.</p>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '16px' }}>
                {associations.map((a) => (
                  <Link key={a.id} to={`/udruge/${a.slug}`} className="card" style={{ padding: '16px', border: '1px solid #eee', borderRadius: 8, textDecoration: 'none', color: 'inherit' }}>
                    <h3 style={{ margin: '0 0 8px' }}>{a.name}</h3>
                    {a.shortDescription && <p style={{ margin: 0, color: '#555' }}>{a.shortDescription}</p>}
                  </Link>
                ))}
              </div>
            )}

            <h2 style={{ marginTop: 32 }}>Fakulteti i akademije</h2>
            {faculties.length === 0 ? (
              <p>Nema pronađenih sastavnica.</p>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '16px' }}>
                {faculties.map((f) => (
                  <Link key={f.slug} to={`/fakulteti/${f.slug}`} className="card" style={{ padding: '16px', border: '1px solid #eee', borderRadius: 8, textDecoration: 'none', color: 'inherit' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--primary-blue)', color: '#fff', display: 'grid', placeItems: 'center', fontWeight: 700 }}>
                        {(f.abbreviation || f.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase())}
                      </div>
                      <h3 style={{ margin: 0 }}>{f.name}</h3>
                    </div>
                    {f.contacts?.address && <p style={{ margin: '8px 0 0', color: '#555' }}>{f.contacts.address}</p>}
                  </Link>
                ))}
              </div>
            )}
          </>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default SearchResultsPage;
