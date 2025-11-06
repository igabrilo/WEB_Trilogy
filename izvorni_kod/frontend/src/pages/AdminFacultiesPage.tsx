import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Faculty } from '../services/api';
import '../css/Dashboard.css';

export default function AdminFacultiesPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user?.role !== 'admin') {
      navigate('/');
      return;
    }

    const loadFaculties = async () => {
      try {
        const res = await apiService.getAllFaculties();
        setFaculties(res.items);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Greška pri učitavanju fakulteta');
      } finally {
        setLoading(false);
      }
    };

    loadFaculties();
  }, [user, navigate]);

  const handleDelete = async (slug: string) => {
    if (!confirm('Jeste li sigurni da želite obrisati ovaj fakultet?')) {
      return;
    }

    try {
      await apiService.deleteFaculty(slug);
      // Reload faculties
      const res = await apiService.getAllFaculties();
      setFaculties(res.items);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Greška pri brisanju fakulteta');
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
              <h1 className="dashboard-title">Upravljanje fakultetima</h1>
              <p className="dashboard-subtitle">Dodajte, uredite ili obrišite fakultete</p>
            </div>
            <div className="dashboard-actions">
              <button className="btn-primary" onClick={() => navigate('/admin/fakulteti/novo')}>
                Dodaj fakultet
              </button>
              <button className="btn-secondary" onClick={() => navigate('/admin')}>
                Natrag na admin panel
              </button>
            </div>
          </div>

          {error && <div className="error-message" style={{ marginBottom: '1.5rem' }}>{error}</div>}

          <div className="dashboard-grid">
            {faculties.map(f => (
              <div key={f.slug} className="dashboard-card">
                <div className="card-header">
                  <div className="card-logo" style={{ background: 'var(--primary-blue)' }}>
                    {f.abbreviation || f.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase()}
                  </div>
                  <span className="card-badge">{f.type === 'academy' ? 'Akademija' : 'Fakultet'}</span>
                </div>
                <h3 className="card-title">{f.name}</h3>
                {f.contacts?.address && <p className="card-description">{f.contacts.address}</p>}
                {f.contacts?.email && <p className="card-description" style={{ marginTop: '0.5rem' }}>📧 {f.contacts.email}</p>}
                <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  <button
                    className="btn-secondary"
                    style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                    onClick={() => navigate(`/admin/fakulteti/${f.slug}/uredi`)}
                  >
                    Uredi
                  </button>
                  <button
                    className="btn-secondary"
                    style={{ fontSize: '0.875rem', padding: '0.5rem 1rem', background: '#fee2e2', color: '#991b1b', border: '1px solid #fecaca' }}
                    onClick={() => handleDelete(f.slug)}
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

