import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import '../css/FormPage.css';

export default function CreateJobPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    type: 'internship' as 'internship' | 'job' | 'part-time' | 'remote',
    company: '',
    location: '',
    salary: '',
    requirements: '',
    tags: '',
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const requirements = formData.requirements.split('\n').filter(r => r.trim());
      const tags = formData.tags.split(',').map(t => t.trim()).filter(t => t);

      await apiService.createJob({
        title: formData.title,
        description: formData.description,
        type: formData.type,
        company: formData.company,
        location: formData.location,
        salary: formData.salary,
        requirements: requirements.length > 0 ? requirements : undefined,
        tags: tags.length > 0 ? tags : undefined,
      });

      navigate('/prakse-i-poslovi');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri kreiranju oglasa');
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

  if (user?.role !== 'employer' && user?.role !== 'poslodavac') {
    return (
      <div className="form-page">
        <Header />
        <main className="form-main">
          <div className="form-container">
            <h1>Pristup odbijen</h1>
            <p>Samo poslodavci mogu kreirati oglase za prakse i poslove.</p>
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
          <h1>Objavi praksu/posao</h1>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="title">Naslov oglasa *</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="npr. Backend Developer Intern"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Opis *</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
                rows={8}
                placeholder="Detaljan opis pozicije..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="type">Tip *</label>
                <select id="type" name="type" value={formData.type} onChange={handleChange} required>
                  <option value="internship">Praksa</option>
                  <option value="job">Posao</option>
                  <option value="part-time">Part-time</option>
                  <option value="remote">Remote</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="company">Tvrtka</label>
                <input
                  type="text"
                  id="company"
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  placeholder="Naziv tvrtke"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="location">Lokacija</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  placeholder="npr. Zagreb"
                />
              </div>

              <div className="form-group">
                <label htmlFor="salary">Plaća</label>
                <input
                  type="text"
                  id="salary"
                  name="salary"
                  value={formData.salary}
                  onChange={handleChange}
                  placeholder="npr. 5000-7000 kn"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="requirements">Uvjeti (svaki u novom redu)</label>
              <textarea
                id="requirements"
                name="requirements"
                value={formData.requirements}
                onChange={handleChange}
                rows={5}
                placeholder="Znanje Python-a&#10;Iskustvo s Flask-om&#10;..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="tags">Oznake (odvojene zarezom)</label>
              <input
                type="text"
                id="tags"
                name="tags"
                value={formData.tags}
                onChange={handleChange}
                placeholder="npr. python, flask, backend"
              />
            </div>

            <div className="form-actions">
              <button type="button" className="btn-secondary" onClick={() => navigate('/prakse-i-poslovi')}>
                Odustani
              </button>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Kreiranje...' : 'Objavi oglas'}
              </button>
            </div>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}

