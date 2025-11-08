import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type ErasmusProject, type Faculty } from '../services/api';
import Header from '../components/Header';
import Footer from '../components/Footer';
import '../css/Dashboard.css';

export default function ErasmusProjectsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [projects, setProjects] = useState<ErasmusProject[]>([]);
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFaculty, setSelectedFaculty] = useState<string>('');
  const [selectedField, setSelectedField] = useState<string>('');

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const [projectsRes, facultiesRes] = await Promise.all([
          apiService.getErasmusProjects({
            faculty: selectedFaculty || undefined,
            fieldOfStudy: selectedField || undefined
          }),
          apiService.getFaculties()
        ]);
        setProjects(projectsRes.items);
        setFaculties(facultiesRes.items);
      } catch (error) {
        console.error('Error loading Erasmus projects:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [selectedFaculty, selectedField]);

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
              <h1 className="dashboard-title">Erasmus projekti</h1>
              <p className="dashboard-subtitle">Pregled dostupnih Erasmus projekata po fakultetima</p>
            </div>
            {user?.role === 'faculty' || user?.role === 'fakultet' ? (
              <button className="btn-primary" onClick={() => navigate('/erasmus/novo')}>
                Objavi Erasmus projekt
              </button>
            ) : null}
          </div>

          <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <select
              value={selectedFaculty}
              onChange={(e) => setSelectedFaculty(e.target.value)}
              style={{
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                fontSize: '1rem',
                minWidth: '200px'
              }}
            >
              <option value="">Svi fakulteti</option>
              {faculties.map(f => (
                <option key={f.slug} value={f.slug}>{f.name}</option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Filtriraj po području studija..."
              value={selectedField}
              onChange={(e) => setSelectedField(e.target.value)}
              style={{
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                fontSize: '1rem',
                flex: 1,
                minWidth: '200px'
              }}
            />
          </div>

          {projects.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
              Nema dostupnih Erasmus projekata.
            </div>
          ) : (
            <div className="dashboard-grid">
              {projects.map(project => (
                <div key={project.id} className="dashboard-card">
                  <div className="card-header">
                    <div className="card-logo" style={{ background: '#1e70bf' }}>
                      EU
                    </div>
                    {project.country && (
                      <span className="card-badge">{project.country}</span>
                    )}
                  </div>
                  <h3 className="card-title">{project.title}</h3>
                  {project.facultyName && (
                    <p className="card-description" style={{ marginTop: '0.5rem' }}>
                      📚 {project.facultyName}
                    </p>
                  )}
                  {project.university && (
                    <p className="card-description" style={{ marginTop: '0.5rem' }}>
                      🏛️ {project.university}
                    </p>
                  )}
                  {project.fieldOfStudy && (
                    <p className="card-description" style={{ marginTop: '0.5rem' }}>
                      📖 {project.fieldOfStudy}
                    </p>
                  )}
                  {project.duration && (
                    <p className="card-description" style={{ marginTop: '0.5rem' }}>
                      ⏱️ {project.duration}
                    </p>
                  )}
                  {project.applicationDeadline && (
                    <p className="card-description" style={{ marginTop: '0.5rem', color: '#dc2626' }}>
                      📅 Rok prijave: {new Date(project.applicationDeadline).toLocaleDateString('hr-HR')}
                    </p>
                  )}
                  <div style={{ marginTop: '1rem' }}>
                    <button
                      className="btn-secondary"
                      style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                      onClick={() => navigate(`/erasmus/${project.id}`)}
                    >
                      Saznaj više
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

