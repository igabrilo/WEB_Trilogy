import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type JobApplication } from '../services/api';
import '../css/Dashboard.css';

export default function JobApplicationsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [applications, setApplications] = useState<JobApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedApp, setSelectedApp] = useState<JobApplication | null>(null);
  const [emailSubject, setEmailSubject] = useState('');
  const [emailMessage, setEmailMessage] = useState('');
  const [sendingEmail, setSendingEmail] = useState(false);

  useEffect(() => {
    if (user?.role !== 'employer' && user?.role !== 'poslodavac') {
      navigate('/');
      return;
    }

    const loadApplications = async () => {
      try {
        const res = await apiService.getJobApplications();
        setApplications(res.items);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Greška pri učitavanju prijava');
      } finally {
        setLoading(false);
      }
    };

    loadApplications();
  }, [user, navigate]);

  const handleStatusUpdate = async (applicationId: number, status: 'approved' | 'rejected') => {
    try {
      await apiService.updateApplicationStatus(applicationId, status);
      // Reload applications
      const res = await apiService.getJobApplications();
      setApplications(res.items);
      setSelectedApp(null);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Greška pri ažuriranju statusa');
    }
  };

  const handleSendEmail = async () => {
    if (!selectedApp || !emailSubject || !emailMessage) {
      alert('Molimo unesite predmet i poruku');
      return;
    }

    setSendingEmail(true);
    try {
      await apiService.sendEmailToApplicant(selectedApp.id, emailSubject, emailMessage);
      alert('Email je poslan!');
      setSelectedApp(null);
      setEmailSubject('');
      setEmailMessage('');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Greška pri slanju emaila');
    } finally {
      setSendingEmail(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const styles: Record<string, { bg: string; color: string }> = {
      pending: { bg: '#fef3c7', color: '#92400e' },
      approved: { bg: '#d1fae5', color: '#065f46' },
      rejected: { bg: '#fee2e2', color: '#991b1b' },
    };
    const style = styles[status] || styles.pending;
    return (
      <span style={{ padding: '0.25rem 0.75rem', borderRadius: '6px', fontSize: '0.875rem', fontWeight: 500, background: style.bg, color: style.color }}>
        {status === 'pending' ? 'Na čekanju' : status === 'approved' ? 'Odobreno' : 'Odbijeno'}
      </span>
    );
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
              <h1 className="dashboard-title">Pregled prijava</h1>
              <p className="dashboard-subtitle">Upravljajte prijavama na vaše oglase</p>
            </div>
            <button className="btn-secondary" onClick={() => navigate('/prakse-i-poslovi')}>
              Natrag na oglase
            </button>
          </div>

          {error && <div className="error-message" style={{ marginBottom: '1.5rem' }}>{error}</div>}

          {applications.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
              <p>Nema prijava trenutno.</p>
            </div>
          ) : (
            <div className="dashboard-grid">
              {applications.map((app) => (
                <div key={app.id} className="dashboard-card">
                  <div className="card-header">
                    <div>
                      <h3 className="card-title">{app.job?.title || 'Nepoznat oglas'}</h3>
                      <p style={{ margin: '0.5rem 0', color: '#64748b' }}>
                        {app.user?.firstName} {app.user?.lastName} ({app.userEmail})
                      </p>
                    </div>
                    {getStatusBadge(app.status)}
                  </div>
                  {app.message && (
                    <p className="card-description" style={{ marginTop: '0.75rem' }}>
                      {app.message}
                    </p>
                  )}
                  <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    {app.status === 'pending' && (
                      <>
                        <button
                          className="btn-primary"
                          style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                          onClick={() => handleStatusUpdate(app.id, 'approved')}
                        >
                          Odobri
                        </button>
                        <button
                          className="btn-secondary"
                          style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                          onClick={() => handleStatusUpdate(app.id, 'rejected')}
                        >
                          Odbij
                        </button>
                      </>
                    )}
                    <button
                      className="btn-secondary"
                      style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                      onClick={() => setSelectedApp(app)}
                    >
                      Pošalji email
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedApp && (
            <div style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'rgba(0, 0, 0, 0.5)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 1000,
            }}>
              <div style={{
                background: 'white',
                padding: '2rem',
                borderRadius: '12px',
                maxWidth: '500px',
                width: '90%',
                maxHeight: '90vh',
                overflow: 'auto',
              }}>
                <h2>Pošalji email korisniku</h2>
                <p style={{ color: '#64748b', marginBottom: '1rem' }}>
                  {selectedApp.user?.firstName} {selectedApp.user?.lastName} ({selectedApp.userEmail})
                </p>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                    Predmet *
                  </label>
                  <input
                    type="text"
                    value={emailSubject}
                    onChange={(e) => setEmailSubject(e.target.value)}
                    style={{ width: '100%', padding: '0.5rem', border: '1px solid #e2e8f0', borderRadius: '6px' }}
                    placeholder="Predmet emaila"
                  />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                    Poruka *
                  </label>
                  <textarea
                    value={emailMessage}
                    onChange={(e) => setEmailMessage(e.target.value)}
                    rows={6}
                    style={{ width: '100%', padding: '0.5rem', border: '1px solid #e2e8f0', borderRadius: '6px' }}
                    placeholder="Poruka..."
                  />
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                  <button
                    className="btn-secondary"
                    onClick={() => {
                      setSelectedApp(null);
                      setEmailSubject('');
                      setEmailMessage('');
                    }}
                  >
                    Odustani
                  </button>
                  <button
                    className="btn-primary"
                    onClick={handleSendEmail}
                    disabled={sendingEmail || !emailSubject || !emailMessage}
                  >
                    {sendingEmail ? 'Slanje...' : 'Pošalji'}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

