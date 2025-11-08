import { useState, useEffect, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Faculty } from '../services/api';
import '../css/FormPage.css';

export default function CreateErasmusProjectPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingFaculties, setLoadingFaculties] = useState(true);
  const [error, setError] = useState('');
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    facultySlug: '',
    country: '',
    university: '',
    fieldOfStudy: '',
    duration: '',
    applicationDeadline: '',
    requirements: '',
    benefits: '',
    contactEmail: '',
    contactPhone: '',
    website: '',
  });

  useEffect(() => {
    if (user?.role !== 'faculty' && user?.role !== 'fakultet') {
      navigate('/');
      return;
    }

    const loadFaculties = async () => {
      try {
        const res = await apiService.getFaculties();
        setFaculties(res.items);
      } catch (error) {
        console.error('Error loading faculties:', error);
      } finally {
        setLoadingFaculties(false);
      }
    };

    loadFaculties();
  }, [user, navigate]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const requirements = formData.requirements.split('\n').filter(r => r.trim());
      const benefits = formData.benefits.split('\n').filter(b => b.trim());

      await apiService.createErasmusProject({
        title: formData.title,
        description: formData.description,
        facultySlug: formData.facultySlug,
        country: formData.country || undefined,
        university: formData.university || undefined,
        fieldOfStudy: formData.fieldOfStudy || undefined,
        duration: formData.duration || undefined,
        applicationDeadline: formData.applicationDeadline || undefined,
        requirements: requirements.length > 0 ? requirements : undefined,
        benefits: benefits.length > 0 ? benefits : undefined,
        contactEmail: formData.contactEmail || undefined,
        contactPhone: formData.contactPhone || undefined,
        website: formData.website || undefined,
      });

      navigate('/erasmus');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri kreiranju Erasmus projekta');
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
            <p>Samo fakulteti mogu kreirati Erasmus projekte.</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  if (loadingFaculties) {
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
          <h1>Objavi novi Erasmus projekt</h1>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="title">Naziv projekta *</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="npr. Erasmus+ razmjena u Njemačkoj"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Opis projekta *</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
                rows={5}
                placeholder="Detaljan opis Erasmus projekta..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="facultySlug">Fakultet *</label>
              <select
                id="facultySlug"
                name="facultySlug"
                value={formData.facultySlug}
                onChange={handleChange}
                required
              >
                <option value="">Odaberi fakultet</option>
                {faculties.map(f => (
                  <option key={f.slug} value={f.slug}>{f.name}</option>
                ))}
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="country">Država</label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  placeholder="npr. Njemačka"
                />
              </div>
              <div className="form-group">
                <label htmlFor="university">Sveučilište</label>
                <input
                  type="text"
                  id="university"
                  name="university"
                  value={formData.university}
                  onChange={handleChange}
                  placeholder="npr. Technical University of Munich"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="fieldOfStudy">Područje studija</label>
                <input
                  type="text"
                  id="fieldOfStudy"
                  name="fieldOfStudy"
                  value={formData.fieldOfStudy}
                  onChange={handleChange}
                  placeholder="npr. Računarstvo"
                />
              </div>
              <div className="form-group">
                <label htmlFor="duration">Trajanje</label>
                <input
                  type="text"
                  id="duration"
                  name="duration"
                  value={formData.duration}
                  onChange={handleChange}
                  placeholder="npr. 1 semestar"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="applicationDeadline">Rok prijave</label>
              <input
                type="date"
                id="applicationDeadline"
                name="applicationDeadline"
                value={formData.applicationDeadline}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="requirements">Uvjeti (svaki u novom redu)</label>
              <textarea
                id="requirements"
                name="requirements"
                value={formData.requirements}
                onChange={handleChange}
                rows={4}
                placeholder="Uvjet 1&#10;Uvjet 2&#10;..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="benefits">Prednosti (svaka u novom redu)</label>
              <textarea
                id="benefits"
                name="benefits"
                value={formData.benefits}
                onChange={handleChange}
                rows={4}
                placeholder="Prednost 1&#10;Prednost 2&#10;..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="contactEmail">Kontakt email</label>
                <input
                  type="email"
                  id="contactEmail"
                  name="contactEmail"
                  value={formData.contactEmail}
                  onChange={handleChange}
                  placeholder="erasmus@fakultet.hr"
                />
              </div>
              <div className="form-group">
                <label htmlFor="contactPhone">Kontakt telefon</label>
                <input
                  type="tel"
                  id="contactPhone"
                  name="contactPhone"
                  value={formData.contactPhone}
                  onChange={handleChange}
                  placeholder="+385 1 234 5678"
                />
              </div>
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

            <div className="form-actions">
              <button type="button" className="btn-secondary" onClick={() => navigate('/erasmus')}>
                Odustani
              </button>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Kreiranje...' : 'Objavi projekt'}
              </button>
            </div>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}

