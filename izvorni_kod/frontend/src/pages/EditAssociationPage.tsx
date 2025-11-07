import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import '../css/FormPage.css';

export default function EditAssociationPage() {
  const { slug } = useParams<{ slug: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState('');
  const [associationId, setAssociationId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    faculty: '',
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

  useEffect(() => {
    if (user?.role !== 'admin' && user?.role !== 'faculty' && user?.role !== 'fakultet') {
      navigate('/');
      return;
    }

    const loadAssociation = async () => {
      if (!slug) return;
      try {
        const res = await apiService.getAssociation(slug);
        const assoc = res.item;
        setAssociationId(assoc.id);
        setFormData({
          name: assoc.name || '',
          faculty: assoc.faculty || '',
          shortDescription: assoc.shortDescription || '',
          description: assoc.description || '',
          type: assoc.type || 'academic',
          logoText: assoc.logoText || '',
          logoBg: assoc.logoBg || '#1e70bf',
          tags: (assoc.tags || []).join(', '),
          website: assoc.links?.website || '',
          facebook: assoc.links?.facebook || '',
          instagram: assoc.links?.instagram || '',
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Greška pri učitavanju udruge');
      } finally {
        setLoadingData(false);
      }
    };

    loadAssociation();
  }, [user, navigate, slug]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!associationId) return;
    setError('');
    setLoading(true);

    try {
      const tags = formData.tags.split(',').map(t => t.trim()).filter(t => t);
      const links: Record<string, string> = {};
      if (formData.website) links.website = formData.website;
      if (formData.facebook) links.facebook = formData.facebook;
      if (formData.instagram) links.instagram = formData.instagram;

      await apiService.updateAssociation(associationId, {
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

      navigate('/admin/udruge');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri ažuriranju udruge');
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

  if (user?.role !== 'admin' && user?.role !== 'faculty' && user?.role !== 'fakultet') {
    return (
      <div className="form-page">
        <Header />
        <main className="form-main">
          <div className="form-container">
            <h1>Pristup odbijen</h1>
            <p>Samo administratori i fakulteti mogu uređivati studentske udruge.</p>
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
          <h1>Uredi studentsku udrugu</h1>
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
              <button type="button" className="btn-secondary" onClick={() => navigate('/admin/udruge')}>
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

