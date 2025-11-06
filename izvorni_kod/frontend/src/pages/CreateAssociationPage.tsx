import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import '../css/FormPage.css';

export default function CreateAssociationPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    faculty: user?.faculty || '',
    shortDescription: '',
    description: '',
    type: 'academic',
    logoText: '',
    logoBg: '#1e70bf',
    tags: '',
    website: '',
    facebook: '',
    instagram: '',
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const tags = formData.tags.split(',').map(t => t.trim()).filter(t => t);
      const links: Record<string, string> = {};
      if (formData.website) links.website = formData.website;
      if (formData.facebook) links.facebook = formData.facebook;
      if (formData.instagram) links.instagram = formData.instagram;

      await apiService.createAssociation({
        name: formData.name,
        faculty: formData.faculty,
        shortDescription: formData.shortDescription,
        description: formData.description,
        type: formData.type,
        logoText: formData.logoText || formData.name.substring(0, 3).toUpperCase(),
        logoBg: formData.logoBg,
        tags,
        links: Object.keys(links).length > 0 ? links : undefined,
      });

      navigate('/udruge');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri kreiranju udruge');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  if (user?.role !== 'faculty' && user?.role !== 'fakultet') {
    return (
      <div className="form-page">
        <Header />
        <main className="form-main">
          <div className="form-container">
            <h1>Pristup odbijen</h1>
            <p>Samo fakulteti mogu kreirati studentske udruge.</p>
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
          <h1>Objavi novu studentsku udrugu</h1>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="name">Naziv udruge *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="npr. AIESEC FER"
              />
            </div>

            <div className="form-group">
              <label htmlFor="faculty">Fakultet *</label>
              <input
                type="text"
                id="faculty"
                name="faculty"
                value={formData.faculty}
                onChange={handleChange}
                required
                placeholder="npr. FER"
              />
            </div>

            <div className="form-group">
              <label htmlFor="shortDescription">Kratki opis *</label>
              <textarea
                id="shortDescription"
                name="shortDescription"
                value={formData.shortDescription}
                onChange={handleChange}
                required
                rows={3}
                placeholder="Kratak opis udruge..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Detaljni opis</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={5}
                placeholder="Detaljni opis udruge..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="type">Tip udruge</label>
                <select id="type" name="type" value={formData.type} onChange={handleChange}>
                  <option value="academic">Akademska</option>
                  <option value="international">Međunarodna</option>
                  <option value="cultural">Kulturna</option>
                  <option value="sports">Sportska</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="logoBg">Boja pozadine logotipa</label>
                <input
                  type="color"
                  id="logoBg"
                  name="logoBg"
                  value={formData.logoBg}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="tags">Oznake (odvojene zarezom)</label>
              <input
                type="text"
                id="tags"
                name="tags"
                value={formData.tags}
                onChange={handleChange}
                placeholder="npr. leadership, international, networking"
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
                placeholder="https://..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="facebook">Facebook</label>
                <input
                  type="url"
                  id="facebook"
                  name="facebook"
                  value={formData.facebook}
                  onChange={handleChange}
                  placeholder="https://facebook.com/..."
                />
              </div>

              <div className="form-group">
                <label htmlFor="instagram">Instagram</label>
                <input
                  type="url"
                  id="instagram"
                  name="instagram"
                  value={formData.instagram}
                  onChange={handleChange}
                  placeholder="https://instagram.com/..."
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="button" className="btn-secondary" onClick={() => navigate('/udruge')}>
                Odustani
              </button>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Kreiranje...' : 'Objavi udrugu'}
              </button>
            </div>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}

