import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type Association } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const AssociationsPage = () => {
  const { user } = useAuth();
  const [items, setItems] = useState<Association[]>([]);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const res = await apiService.getAssociations({ faculty: user?.faculty || undefined, q });
      setItems(res.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.faculty]);

  return (
    <div className="associations-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Studentske udruge {user?.faculty ? `- ${user.faculty}` : ''}</h1>
        <div style={{ display: 'flex', gap: '8px', margin: '12px 0' }}>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Pretraži udruge..."
            className="form-input"
            style={{ flex: 1 }}
          />
          <button className="btn-primary" onClick={load}>Pretraži</button>
        </div>
        {loading ? (
          <p>Učitavanje...</p>
        ) : items.length === 0 ? (
          <p>Nema rezultata.</p>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '16px' }}>
            {items.map((a) => (
              <Link key={a.id} to={`/udruge/${a.slug}`} className="card" style={{ padding: '16px', border: '1px solid #eee', borderRadius: 8, textDecoration: 'none', color: 'inherit' }}>
                <h3 style={{ margin: '0 0 8px' }}>{a.name}</h3>
                {a.shortDescription && <p style={{ margin: 0, color: '#555' }}>{a.shortDescription}</p>}
                {a.tags && (
                  <div style={{ marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {a.tags.slice(0, 4).map((t) => (
                      <span key={t} style={{ background: '#f1f5f9', padding: '2px 8px', borderRadius: 999, fontSize: 12 }}>{t}</span>
                    ))}
                  </div>
                )}
              </Link>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default AssociationsPage;
