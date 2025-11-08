import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type ErasmusProject } from '../services/api';
import '../css/FormPage.css';

export default function ErasmusProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<ErasmusProject | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProject = async () => {
      if (!id) return;
      try {
        const res = await apiService.getErasmusProject(parseInt(id));
        setProject(res.item);
      } catch (err) {
        console.error('Error loading project:', err);
      } finally {
        setLoading(false);
      }
    };

    loadProject();
  }, [id]);

  if (loading) {
    return (
      <div className="form-page">
        <Header />
        <main className="form-main">
          <div className="form-container">
            <p>Učitavanje...</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  if (!project) {
    return (
      <div className="form-page">
        <Header />
        <main className="form-main">
          <div className="form-container">
            <h1>Projekt nije pronađen</h1>
            <button className="btn-secondary" onClick={() => navigate('/erasmus')}>
              Natrag na Erasmus projekte
            </button>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="form-page">
      <Header />
      <main className="form-main">
        <div className="form-container" style={{ maxWidth: '800px' }}>
          <button 
            className="btn-secondary" 
            onClick={() => navigate('/erasmus')}
            style={{ marginBottom: '1.5rem' }}
          >
            ← Natrag na Erasmus projekte
          </button>

          <div style={{ 
            background: 'white', 
            borderRadius: '12px', 
            padding: '2rem', 
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '2rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
              <div>
                <span style={{ 
                  display: 'inline-block',
                  padding: '0.25rem 0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  background: '#e0e7ff',
                  color: '#4338ca',
                  marginBottom: '0.5rem'
                }}>
                  Erasmus+ Projekt
                </span>
                <h1 style={{ margin: '0.5rem 0', fontSize: '1.875rem', fontWeight: 700 }}>
                  {project.title}
                </h1>
                {project.facultyName && (
                  <p style={{ margin: '0.5rem 0', fontSize: '1.125rem', color: '#64748b' }}>
                    📚 {project.facultyName}
                  </p>
                )}
              </div>
            </div>

            <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', marginBottom: '1.5rem', paddingBottom: '1.5rem', borderBottom: '1px solid #e2e8f0' }}>
              {project.country && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b' }}>
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
                    <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                    <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                  </svg>
                  <span>{project.country}</span>
                </div>
              )}
              {project.university && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b' }}>
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
                    <path d="M2 4h12M2 8h12M2 12h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                  <span>{project.university}</span>
                </div>
              )}
              {project.duration && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b' }}>
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1v7l4 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" />
                  </svg>
                  <span>{project.duration}</span>
                </div>
              )}
              {project.applicationDeadline && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#dc2626', fontWeight: 600 }}>
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1v7l4 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" />
                  </svg>
                  <span>Rok: {new Date(project.applicationDeadline).toLocaleDateString('hr-HR')}</span>
                </div>
              )}
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Opis projekta</h2>
              <p style={{ color: '#475569', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                {project.description}
              </p>
            </div>

            {project.fieldOfStudy && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Područje studija</h2>
                <p style={{ color: '#475569' }}>{project.fieldOfStudy}</p>
              </div>
            )}

            {project.requirements && project.requirements.length > 0 && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Uvjeti</h2>
                <ul style={{ color: '#475569', lineHeight: '1.8', paddingLeft: '1.5rem' }}>
                  {project.requirements.map((req, idx) => (
                    <li key={idx}>{req}</li>
                  ))}
                </ul>
              </div>
            )}

            {project.benefits && project.benefits.length > 0 && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Prednosti</h2>
                <ul style={{ color: '#475569', lineHeight: '1.8', paddingLeft: '1.5rem' }}>
                  {project.benefits.map((benefit, idx) => (
                    <li key={idx}>{benefit}</li>
                  ))}
                </ul>
              </div>
            )}

            {(project.contactEmail || project.contactPhone || project.website) && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Kontakt</h2>
                {project.contactEmail && (
                  <p style={{ color: '#475569', marginBottom: '0.5rem' }}>
                    📧 <a href={`mailto:${project.contactEmail}`} style={{ color: '#1e70bf' }}>{project.contactEmail}</a>
                  </p>
                )}
                {project.contactPhone && (
                  <p style={{ color: '#475569', marginBottom: '0.5rem' }}>
                    📞 {project.contactPhone}
                  </p>
                )}
                {project.website && (
                  <p style={{ color: '#475569' }}>
                    🌐 <a href={project.website} target="_blank" rel="noopener noreferrer" style={{ color: '#1e70bf' }}>{project.website}</a>
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

