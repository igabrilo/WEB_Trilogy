import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService, type LoginCredentials } from '../services/api';
import '../css/LoginPage.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState<LoginCredentials>({
    email: '',
    password: '',
  });
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // First check if AAI login is required
      const response = await apiService.login(formData);

      // Check if AAI login is required (faculty email detected)
      if (response.requires_aai && response.aai_login_url) {
        // Redirect to AAI login
        window.location.href = response.aai_login_url;
        return;
      }

      // If we get here, it's a successful login (AAI check passed or not needed)
      // Use the AuthContext login which handles token storage
      await login(formData);
      // Redirect to home page on successful login
      navigate('/');
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

  return (
    <div className="login-page">
      <Header />
      <main className="login-main">
        <section className="login-hero">
          <div className="login-hero-container fade-in">
            <h1 className="login-hero-title slide-up">Prijava</h1>
            <p className="login-hero-subtitle slide-up" style={{ animationDelay: '0.1s' }}>
              Prijavite se na svoj račun da biste pristupili svim funkcijama
            </p>
          </div>
        </section>

        <section className="login-content">
          <div className="login-container">
            <div className="login-card slide-up" style={{ animationDelay: '0.2s' }}>
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
                    'Prijavi se'
                  )}
                </button>

                <div className="login-divider">
                  <span>ili</span>
                </div>

                <p className="register-prompt">
                  Nemate račun?{' '}
                  <Link to="/registracija" className="register-link">
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

