import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Association } from '../services/api';
import '../css/Dashboard.css';

export default function AdminAssociationsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [associations, setAssociations] = useState<Association[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user?.role !== 'admin') {
      navigate('/');
      return;
    }

    const loadAssociations = async () => {
      try {
        const res = await apiService.getAllAssociations();
        setAssociations(res.items);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Greška pri učitavanju udruga');
      } finally {
        setLoading(false);
      }
    };

    loadAssociations();
  }, [user, navigate]);

  const handleDelete = async (associationId: number) => {
    if (!confirm('Jeste li sigurni da želite obrisati ovu udrugu?')) {
      return;
    }

    try {
      await apiService.deleteAssociation(associationId);
      // Reload associations
      const res = await apiService.getAllAssociations();
      setAssociations(res.items);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Greška pri brisanju udruge');
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <Header />
        <main className="dashboard-main">
          <div className="dashboard-container">
            <p>Učitavanje...</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <Header />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Upravljanje studentskim udrugama</h1>
              <p className="dashboard-subtitle">Dodajte, uredite ili obrišite studentske udruge</p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/udruge/novo')}>
                Dodaj udrugu
              </button>
              <button className="btn-secondary" onClick={() => navigate('/admin')}>
                Natrag na admin panel
              </button>
            </div>
          </div>

          {error && <div className="error-message" style={{ marginBottom: '1.5rem' }}>{error}</div>}

          <div className="dashboard-grid">
            {associations.map(a => (
              <div key={a.id} className="dashboard-card">
                <div className="card-header">
                  <div className="card-logo" style={{ background: a.logoBg || '#1e293b' }}>
                    {a.logoText || (a.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase())}
                  </div>
                  {a.faculty && <span className="card-badge">{a.faculty}</span>}
                </div>
                <h3 className="card-title">{a.name}</h3>
                {a.shortDescription && <p className="card-description">{a.shortDescription}</p>}
                <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  <button
                    className="btn-secondary"
                    style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                    onClick={() => navigate(`/udruge/${a.slug}/uredi`)}
                  >
                    Uredi
                  </button>
                  <button
                    className="btn-secondary"
                    style={{ fontSize: '0.875rem', padding: '0.5rem 1rem', background: '#fee2e2', color: '#991b1b', border: '1px solid #fecaca' }}
                    onClick={() => handleDelete(a.id)}
                  >
                    Obriši
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

