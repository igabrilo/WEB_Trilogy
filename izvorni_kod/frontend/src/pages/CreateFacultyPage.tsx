import { useState, useEffect, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import '../css/FormPage.css';

export default function CreateFacultyPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    abbreviation: '',
    type: 'faculty' as 'faculty' | 'academy',
    email: '',
    phone: '',
    address: '',
    website: '',
  });

  useEffect(() => {
    if (user?.role !== 'admin') {
      navigate('/');
    }
  }, [user, navigate]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await apiService.createFaculty({
        name: formData.name,
        abbreviation: formData.abbreviation,
        type: formData.type,
        email: formData.email || undefined,
        phone: formData.phone || undefined,
        address: formData.address || undefined,
        website: formData.website || undefined,
      });

      navigate('/admin');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri kreiranju fakulteta');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  if (user?.role !== 'admin') {
    return (
      <div className="form-page">
        <Header />
        <main className="form-main">
          <div className="form-container">
            <h1>Pristup odbijen</h1>
            <p>Samo administratori mogu dodavati fakultete.</p>
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
        <div className="form-container">
          <h1>Dodaj novi fakultet</h1>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="name">Naziv fakulteta *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="npr. Fakultet elektrotehnike i računarstva"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="abbreviation">Skraćenica</label>
                <input
                  type="text"
                  id="abbreviation"
                  name="abbreviation"
                  value={formData.abbreviation}
                  onChange={handleChange}
                  placeholder="npr. FER"
                />
              </div>

              <div className="form-group">
                <label htmlFor="type">Tip *</label>
                <select id="type" name="type" value={formData.type} onChange={handleChange} required>
                  <option value="faculty">Fakultet</option>
                  <option value="academy">Akademija</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="info@fakultet.hr"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="phone">Telefon</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder="+385 1 234 5678"
                />
              </div>

              <div className="form-group">
                <label htmlFor="website">Web stranica</label>
                <input
                  type="url"
                  id="website"
                  name="website"
                  value={formData.website}
                  onChange={handleChange}
                  placeholder="https://www.fakultet.unizg.hr"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="address">Adresa</label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Ulica i broj, 10000 Zagreb"
              />
            </div>

            <div className="form-actions">
              <button type="button" className="btn-secondary" onClick={() => navigate('/admin')}>
                Odustani
              </button>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Kreiranje...' : 'Dodaj fakultet'}
              </button>
            </div>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}

