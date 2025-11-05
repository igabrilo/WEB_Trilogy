import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type Association } from '../services/api';

const AssociationDetailPage = () => {
  const { slug } = useParams();
  const [assoc, setAssoc] = useState<Association | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const run = async () => {
      if (!slug) return;
      setLoading(true);
      setError(null);
      try {
        const res = await apiService.getAssociation(slug);
        setAssoc(res.item);
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Greška učitavanja');
      } finally {
        setLoading(false);
      }
    };
    run();
  }, [slug]);

  return (
    <div className="association-detail-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem', maxWidth: 900 }}>
        <Link to="/udruge" style={{ textDecoration: 'none', color: '#1e70bf' }}>&larr; Natrag na udruge</Link>
        {loading ? (
          <p>Učitavanje...</p>
        ) : error ? (
          <p style={{ color: 'red' }}>{error}</p>
        ) : assoc ? (
          <article>
            <h1 style={{ marginBottom: 8 }}>{assoc.name}</h1>
            {assoc.faculty && <div style={{ color: '#475569', marginBottom: 16 }}>Fakultet: {assoc.faculty}</div>}
            {assoc.tags && (
              <div style={{ marginBottom: 16, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {assoc.tags.map((t) => (
                  <span key={t} style={{ background: '#f1f5f9', padding: '2px 8px', borderRadius: 999, fontSize: 12 }}>{t}</span>
                ))}
              </div>
            )}
            {assoc.description && <p style={{ lineHeight: 1.6 }}>{assoc.description}</p>}
            {assoc.links && (
              <div style={{ marginTop: 16 }}>
                {Object.entries(assoc.links).map(([k, v]) => (
                  <a key={k} href={v} target="_blank" rel="noreferrer" style={{ marginRight: 12, color: '#1e70bf' }}>
                    {k}
                  </a>
                ))}
              </div>
            )}
          </article>
        ) : null}
      </main>
      <Footer />
    </div>
  );
};

export default AssociationDetailPage;
