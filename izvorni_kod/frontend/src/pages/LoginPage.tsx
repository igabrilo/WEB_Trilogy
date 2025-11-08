import { useState, useEffect, useMemo } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type LoginCredentials } from '../services/api';
import '../css/LoginPage.css';
import '../css/Hero.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { login, refreshUser } = useAuth();
  const [formData, setFormData] = useState<LoginCredentials>({
    email: '',
    password: '',
  });
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isGoogleLoading, setIsGoogleLoading] = useState<boolean>(false);

  const selectedRole = (searchParams.get('role') || '').toLowerCase();
  const ROLE_LABELS: Record<string, string> = {
    ucenik: 'Učenik',
    student: 'Student',
    alumni: 'Alumni',
    employer: 'Poslodavac',
    faculty: 'Fakultet',
  };
  const roleLabel = useMemo(() => (selectedRole ? ROLE_LABELS[selectedRole] || '' : ''), [selectedRole]);

  // Determine which login options to show based on role
  // AAI login is optional for all roles (not required)
  const showGoogleLogin = true; // Allow Google login for all roles
  const showAAILogin = selectedRole === 'faculty' || selectedRole === 'fakultet'; // Show AAI option for faculty, but email/password is also allowed

  // Handle OAuth callback if token is in URL
  useEffect(() => {
    const token = searchParams.get('token');
    const oauthError = searchParams.get('error');

    if (oauthError) {
      const decodedError = decodeURIComponent(oauthError);
      setError(decodedError || 'Google prijava nije uspjela. Pokušajte ponovno.');
      // Clean URL
      window.history.replaceState({}, '', '/prijava');
      return;
    }

    if (token) {
      // Token received from OAuth callback
      const userStr = searchParams.get('user');
      if (userStr) {
        try {
          const decodedUserStr = decodeURIComponent(userStr);
          const user = JSON.parse(decodedUserStr);
          localStorage.setItem('token', token);
          localStorage.setItem('user', JSON.stringify(user));
          // Refresh user in context and wait for it to complete
          refreshUser().then(() => {
            // Small delay to ensure state is updated
            setTimeout(() => {
              // Clean URL and redirect to home page
              window.history.replaceState({}, '', '/prijava');
              navigate('/');
            }, 100);
          }).catch(() => {
            // Even if refresh fails, redirect (user data is in localStorage)
            window.history.replaceState({}, '', '/prijava');
            navigate('/');
          });
        } catch (e) {
          setError('Greška pri obradi Google prijave.');
          window.history.replaceState({}, '', '/prijava');
        }
      }
    }
  }, [searchParams, navigate, refreshUser]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Regular email/password login (AAI login is optional, not required)
      // Use the AuthContext login which handles token storage
      await login(formData);
      // Small delay to ensure state is updated before navigation
      setTimeout(() => {
        // Redirect to home page which will show the appropriate dashboard
        navigate('/');
      }, 100);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during login');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleGoogleLogin = async () => {
    // Google login is allowed for all roles including faculty

    setError('');
    setIsGoogleLoading(true);
    try {
      await apiService.initiateGoogleLogin();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri Google prijavi');
      setIsGoogleLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Header />
      <main className="login-main">
        <section className="login-hero">
          <div className="login-hero-container fade-in">
            <h1 className="login-hero-title slide-up">
              {selectedRole ? `Prijava — ${roleLabel}` : 'Prijava — odaberite kategoriju'}
            </h1>
            <p className="login-hero-subtitle slide-up" style={{ animationDelay: '0.1s' }}>
              Prijavite se na svoj račun da biste pristupili svim funkcijama
            </p>
          </div>
        </section>

        <section className="login-content">
          {!selectedRole && (
            <div className="profile-selection-container auth-profile-picker" style={{ marginBottom: 24 }}>
              <div className="profile-grid">
                {(['ucenik', 'student', 'alumni', 'employer', 'faculty'] as const).map((r) => (
                  <div
                    key={r}
                    className="profile-card animate-in"
                    role="button"
                    tabIndex={0}
                    onClick={() => navigate(`/prijava?role=${r}`)}
                    onKeyDown={(e) => { if (e.key === 'Enter') navigate(`/prijava?role=${r}`); }}
                  >
                    <div className="profile-icon blue-icon">
                      <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                        <circle cx="24" cy="24" r="10" stroke="currentColor" strokeWidth="2.5" />
                      </svg>
                    </div>
                    <h3 className="profile-card-title">{ROLE_LABELS[r]}</h3>
                    <p className="profile-card-subtitle">Odaberite {ROLE_LABELS[r].toLowerCase()} profil</p>
                  </div>
                ))}
              </div>
            </div>
          )}
          <div className="login-container">
            <div className="login-card slide-up" style={{ animationDelay: '0.2s' }}>
              {selectedRole && (
                <div className="info-banner" style={{ marginBottom: 16, fontWeight: 500 }}>
                  Prijavljujete se kao: {roleLabel}
                </div>
              )}
              <form onSubmit={handleSubmit} className="login-form">
                {error && (
                  <div className="error-message">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2" />
                      <path d="M10 6v4M10 14h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    {error}
                  </div>
                )}

                <div className="form-group">
                  <label htmlFor="email">Email adresa</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="vas.email@example.com"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="password">Lozinka</label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    placeholder="Unesite lozinku"
                    className="form-input"
                  />
                </div>

                <div className="form-options">
                  <label className="checkbox-label">
                    <input type="checkbox" />
                    <span>Zapamti me</span>
                  </label>
                  <Link to="/forgot-password" className="forgot-link">
                    Zaboravili ste lozinku?
                  </Link>
                </div>

                <button
                  type="submit"
                  className="login-btn"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <svg className="spinner" width="20" height="20" viewBox="0 0 20 20">
                        <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="50" strokeDashoffset="25">
                          <animate attributeName="stroke-dashoffset" values="25;0;25" dur="1.5s" repeatCount="indefinite" />
                        </circle>
                      </svg>
                      Prijavljivanje...
                    </>
                  ) : (
                    showAAILogin ? 'Prijavi se preko AAI@EduHr' : 'Prijavi se'
                  )}
                </button>

                {showGoogleLogin && (
                  <>
                    <div className="login-divider">
                      <span>ili</span>
                    </div>

                    <button
                      type="button"
                      className="google-login-btn"
                      onClick={handleGoogleLogin}
                      disabled={isGoogleLoading || isLoading}
                    >
                      {isGoogleLoading ? (
                        <>
                          <svg className="spinner" width="20" height="20" viewBox="0 0 20 20">
                            <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="50" strokeDashoffset="25">
                              <animate attributeName="stroke-dashoffset" values="25;0;25" dur="1.5s" repeatCount="indefinite" />
                            </circle>
                          </svg>
                          Prijavljivanje...
                        </>
                      ) : (
                        <>
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                          </svg>
                          Prijavi se s Google računom
                        </>
                      )}
                    </button>
                  </>
                )}

                {showAAILogin && (
                  <div style={{ marginTop: '1rem', padding: '1rem', background: '#f0f9ff', borderRadius: '8px', border: '1px solid #bae6fd' }}>
                    <p style={{ margin: 0, fontSize: '0.875rem', color: '#0c4a6e' }}>
                      <strong>Napomena:</strong> Fakulteti se mogu prijaviti koristeći email i lozinku ili preko AAI@EduHr sustava.
                      AAI@EduHr prijava je opcija za korisnike s fakultetskom email adresom.
                    </p>
                  </div>
                )}

                <p className="register-prompt">
                  Nemate račun?{' '}
                  <Link to={`/registracija${selectedRole ? `?role=${selectedRole}` : ''}`} className="register-link">
                    Registrirajte se
                  </Link>
                </p>
              </form>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default LoginPage;

