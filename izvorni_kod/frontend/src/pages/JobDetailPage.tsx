import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Job } from '../services/api';
import '../css/FormPage.css';

export default function JobDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const loadJob = async () => {
      if (!id) return;
      try {
        const res = await apiService.getJob(parseInt(id));
        setJob(res.item);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Greška pri učitavanju posla');
      } finally {
        setLoading(false);
      }
    };

    loadJob();
  }, [id]);

  const handleApply = async (e: FormEvent) => {
    e.preventDefault();
    if (!id || !isAuthenticated) {
      navigate('/prijava');
      return;
    }

    setError('');
    setApplying(true);

    try {
      await apiService.applyToJob(parseInt(id), message || undefined);
      setSuccess(true);
      setMessage('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri prijavi na posao');
    } finally {
      setApplying(false);
    }
  };

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

  if (!job) {
    return (
      <div className="form-page">
        <Header />
        <main className="form-main">
          <div className="form-container">
            <h1>Posao nije pronađen</h1>
            <button className="btn-secondary" onClick={() => navigate('/prakse-i-poslovi')}>
              Natrag na poslove
            </button>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  const typeLabel = job.type === 'internship' ? 'Praksa' :
    job.type === 'job' ? 'Posao' :
      job.type === 'part-time' ? 'Djelomično radno vrijeme' :
        job.type === 'remote' ? 'Udaljeno' : job.type;

  return (
    <div className="form-page">
      <Header />
      <main className="form-main">
        <div className="form-container" style={{ maxWidth: '800px' }}>
          <button 
            className="btn-secondary" 
            onClick={() => navigate('/prakse-i-poslovi')}
            style={{ marginBottom: '1.5rem' }}
          >
            ← Natrag na poslove
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
                  {typeLabel}
                </span>
                <h1 style={{ margin: '0.5rem 0', fontSize: '1.875rem', fontWeight: 700 }}>
                  {job.title}
                </h1>
                {job.company && (
                  <p style={{ margin: '0.5rem 0', fontSize: '1.125rem', color: '#64748b' }}>
                    {job.company}
                  </p>
                )}
              </div>
            </div>

            <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', marginBottom: '1.5rem', paddingBottom: '1.5rem', borderBottom: '1px solid #e2e8f0' }}>
              {job.location && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b' }}>
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
                    <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                    <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                  </svg>
                  <span>{job.location}</span>
                </div>
              )}
              {job.salary && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#059669', fontWeight: 600 }}>
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1v14M3 6h10M3 10h10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                  <span>{job.salary}</span>
                </div>
              )}
              {job.createdAt && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b' }}>
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1v7l4 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" />
                  </svg>
                  <span>Objavljeno: {new Date(job.createdAt).toLocaleDateString('hr-HR')}</span>
                </div>
              )}
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Opis posla</h2>
              <p style={{ color: '#475569', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                {job.description}
              </p>
            </div>

            {job.requirements && job.requirements.length > 0 && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Uvjeti</h2>
                <ul style={{ color: '#475569', lineHeight: '1.8', paddingLeft: '1.5rem' }}>
                  {job.requirements.map((req, idx) => (
                    <li key={idx}>{req}</li>
                  ))}
                </ul>
              </div>
            )}

            {job.tags && job.tags.length > 0 && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Oznake</h2>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {job.tags.map((tag, idx) => (
                    <span 
                      key={idx}
                      style={{
                        padding: '0.375rem 0.75rem',
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        background: '#f1f5f9',
                        color: '#475569'
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {success ? (
            <div style={{ 
              background: '#d1fae5', 
              border: '1px solid #86efac', 
              borderRadius: '8px', 
              padding: '1.5rem',
              marginBottom: '1.5rem'
            }}>
              <h3 style={{ color: '#065f46', marginBottom: '0.5rem' }}>✓ Uspješno ste se prijavili!</h3>
              <p style={{ color: '#047857', margin: 0 }}>
                Vaša prijava je zaprimljena. Poslodavac će vas kontaktirati ukoliko budete odabrani.
              </p>
            </div>
          ) : isAuthenticated ? (
            <div style={{ 
              background: 'white', 
              borderRadius: '12px', 
              padding: '2rem', 
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1rem' }}>
                Prijavi se na ovaj posao
              </h2>
              {error && (
                <div className="error-message" style={{ marginBottom: '1rem' }}>
                  {error}
                </div>
              )}
              <form onSubmit={handleApply} className="form">
                <div className="form-group">
                  <label htmlFor="message">Poruka poslodavcu (opcionalno)</label>
                  <textarea
                    id="message"
                    name="message"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    rows={5}
                    placeholder="Napišite kratku poruku poslodavcu o sebi i zašto ste zainteresirani za ovaj posao..."
                    style={{ width: '100%', padding: '0.75rem', border: '1px solid #cbd5e1', borderRadius: '6px', fontSize: '1rem' }}
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-primary" disabled={applying}>
                    {applying ? 'Prijavljivanje...' : 'Prijavi se'}
                  </button>
                </div>
              </form>
            </div>
          ) : (
            <div style={{ 
              background: '#fef3c7', 
              border: '1px solid #fde68a', 
              borderRadius: '8px', 
              padding: '1.5rem',
              textAlign: 'center'
            }}>
              <p style={{ color: '#92400e', marginBottom: '1rem' }}>
                Morate biti prijavljeni da biste se mogli prijaviti na posao.
              </p>
              <button className="btn-primary" onClick={() => navigate('/prijava')}>
                Prijavi se
              </button>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

