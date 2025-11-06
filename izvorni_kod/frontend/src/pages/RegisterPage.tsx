import { useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import type { RegisterData } from '../services/api';
import '../css/RegisterPage.css';
import '../css/Hero.css';

const RegisterPage = () => {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const { register } = useAuth();
  const [formData, setFormData] = useState<RegisterData>({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    role: 'student',
    faculty: 'FER',
    interests: [],
  });
  const selectedRole = useMemo(() => (params.get('role') || '').toLowerCase(), [params]);
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const ROLE_LABELS: Record<string, string> = {
    ucenik: 'Učenik',
    student: 'Student',
    alumni: 'Alumni',
    employer: 'Poslodavac',
    faculty: 'Fakultet',
  };
  const roleLabel = useMemo(() => (selectedRole ? ROLE_LABELS[selectedRole] || '' : ''), [selectedRole]);

  useEffect(() => {
    if (selectedRole) {
      setFormData((prev) => ({ ...prev, role: selectedRole }));
    }
  }, [selectedRole]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (formData.password !== confirmPassword) {
      setError('Lozinke se ne podudaraju');
      return;
    }

    if (formData.password.length < 6) {
      setError('Lozinka mora imati najmanje 6 znakova');
      return;
    }

    setIsLoading(true);

    try {
  await register(formData);
  // Redirect to role-specific landing
  const role = formData.role || selectedRole || 'student';
  navigate(`/profil/${role}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Došlo je do greške tijekom registracije');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    if (e.target.name === 'confirmPassword') {
      setConfirmPassword(e.target.value);
    } else {
      const name = e.target.name;
      const value = e.target.value;
      if (name === 'interestsText') {
        // handled separately
      }
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  return (
    <div className="register-page">
      <Header />
      <main className="register-main">
        <section className="register-hero">
          <div className="register-hero-container fade-in">
            <h1 className="register-hero-title slide-up">{selectedRole ? `Registracija — ${roleLabel}` : 'Registracija — odaberite kategoriju'}</h1>
            <p className="register-hero-subtitle slide-up" style={{ animationDelay: '0.1s' }}>
              Kreirajte svoj račun i započnite svoju karijeru već danas
            </p>
          </div>
        </section>

        <section className="register-content">
          {!selectedRole && (
            <div className="profile-selection-container auth-profile-picker" style={{ marginBottom: 24 }}>
              <div className="profile-grid">
                {(['ucenik','student','alumni','employer','faculty'] as const).map((r) => (
                  <div
                    key={r}
                    className="profile-card animate-in"
                    role="button"
                    tabIndex={0}
                    onClick={() => navigate(`/registracija?role=${r}`)}
                    onKeyDown={(e) => { if (e.key === 'Enter') navigate(`/registracija?role=${r}`); }}
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
          <div className="register-container">
            <div className="register-card slide-up" style={{ animationDelay: '0.2s' }}>
              {selectedRole && (
                <div className="info-banner" style={{ marginBottom: 16, fontWeight: 500 }}>
                  Registrirate se kao: {roleLabel}
                </div>
              )}
              <form onSubmit={handleSubmit} className="register-form">
                {error && (
                  <div className="error-message">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2" />
                      <path d="M10 6v4M10 14h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    {error}
                  </div>
                )}

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">Ime</label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      required
                      placeholder="Vaše ime"
                      className="form-input"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="lastName">Prezime</label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      required
                      placeholder="Vaše prezime"
                      className="form-input"
                    />
                  </div>
                </div>

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
                  <label htmlFor="role">Tip korisnika</label>
                  <select
                    id="role"
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    className="form-input"
                    disabled={!!selectedRole}
                  >
                    <option value="student">Student</option>
                    <option value="alumni">Alumni</option>
                    <option value="ucenik">Učenik</option>
                    <option value="employer">Poslodavac</option>
                    <option value="faculty">Fakultet</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="faculty">Fakultet</label>
                  <select
                    id="faculty"
                    name="faculty"
                    value={formData.faculty}
                    onChange={handleChange}
                    className="form-input"
                  >
                    <option value="FER">FER</option>
                    <option value="FFZG">FFZG</option>
                    <option value="PMF">PMF</option>
                    <option value="EFZG">EFZG</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="interests">Interesi (zarezom odvojeni)</label>
                  <input
                    type="text"
                    id="interestsText"
                    name="interestsText"
                    placeholder="npr. elektronika, robotika, AI"
                    className="form-input"
                    onChange={(e) => setFormData({ ...formData, interests: e.target.value.split(',').map(s => s.trim()).filter(Boolean) })}
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
                    minLength={6}
                    placeholder="Najmanje 6 znakova"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="confirmPassword">Potvrdi lozinku</label>
                  <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    value={confirmPassword}
                    onChange={handleChange}
                    required
                    placeholder="Potvrdite lozinku"
                    className="form-input"
                  />
                </div>

                <div className="form-terms">
                  <label className="checkbox-label">
                    <input type="checkbox" required />
                    <span>
                      Prihvaćam{' '}
                      <Link to="/terms" className="terms-link">
                        uvjete korištenja
                      </Link>{' '}
                      i{' '}
                      <Link to="/privacy" className="terms-link">
                        pravila privatnosti
                      </Link>
                    </span>
                  </label>
                </div>

                <button
                  type="submit"
                  className="register-btn"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <svg className="spinner" width="20" height="20" viewBox="0 0 20 20">
                        <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="50" strokeDashoffset="25">
                          <animate attributeName="stroke-dashoffset" values="25;0;25" dur="1.5s" repeatCount="indefinite" />
                        </circle>
                      </svg>
                      Registracija...
                    </>
                  ) : (
                    'Registriraj se'
                  )}
                </button>

                <div className="register-divider">
                  <span>ili</span>
                </div>

                <p className="login-prompt">
                  Već imate račun?{' '}
                  <Link to={`/prijava${selectedRole ? `?role=${selectedRole}` : ''}`} className="login-link">
                    Prijavite se
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

export default RegisterPage;

