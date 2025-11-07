import { useState, useEffect, type FormEvent } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import '../css/FormPage.css';

export default function EditFacultyPage() {
  const { slug } = useParams<{ slug: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
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
      return;
    }

    const loadFaculty = async () => {
      if (!slug) return;
      try {
        const res = await apiService.getFaculty(slug);
        const faculty = res.item;
        setFormData({
          name: faculty.name || '',
          abbreviation: faculty.abbreviation || '',
          type: (faculty.type as 'faculty' | 'academy') || 'faculty',
          email: faculty.contacts?.email || '',
          phone: faculty.contacts?.phone || '',
          address: faculty.contacts?.address || '',
          website: faculty.contacts?.website || '',
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Greška pri učitavanju fakulteta');
      } finally {
        setLoadingData(false);
      }
    };

    loadFaculty();
  }, [user, navigate, slug]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!slug) return;
    setError('');
    setLoading(true);

    try {
      await apiService.updateFaculty(slug, {
        name: formData.name,
        abbreviation: formData.abbreviation,
        type: formData.type,
        email: formData.email || undefined,
        phone: formData.phone || undefined,
        address: formData.address || undefined,
        website: formData.website || undefined,
      });

      navigate('/admin/fakulteti');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri ažuriranju fakulteta');
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
            <p>Samo administratori mogu uređivati fakultete.</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  if (loadingData) {
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

  return (
    <div className="form-page">
      <Header />
      <main className="form-main">
        <div className="form-container">
          <h1>Uredi fakultet</h1>
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
              <button type="button" className="btn-secondary" onClick={() => navigate('/admin/fakulteti')}>
                Odustani
              </button>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Spremanje...' : 'Spremi promjene'}
              </button>
            </div>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}

