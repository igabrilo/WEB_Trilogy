import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import '../css/FormPage.css';

export default function EditProfilePage() {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    faculty: '',
    interests: [] as string[],
    interestsInput: '',
  });

  useEffect(() => {
    if (user) {
      setFormData({
        firstName: user.firstName || '',
        lastName: user.lastName || '',
        username: user.username || '',
        faculty: user.faculty || '',
        interests: user.interests || [],
        interestsInput: (user.interests || []).join(', '),
      });
      setLoadingData(false);
    }
  }, [user]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!user) return;
    setError('');
    setSuccess(false);
    setLoading(true);

    try {
      const interests = formData.interestsInput.split(',').map(i => i.trim()).filter(i => i);
      
      const updateData: any = {};
      if (user.role === 'employer' || user.role === 'poslodavac' || user.role === 'faculty' || user.role === 'fakultet') {
        if (formData.username) updateData.username = formData.username;
      } else {
        if (formData.firstName) updateData.firstName = formData.firstName;
        if (formData.lastName) updateData.lastName = formData.lastName;
      }
      if (formData.faculty) updateData.faculty = formData.faculty;
      if (interests.length > 0) updateData.interests = interests;

      await apiService.updateProfile(updateData);
      await refreshUser();
      setSuccess(true);
      setTimeout(() => {
        navigate('/profil');
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Greška pri ažuriranju profila');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

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

  const isInstitutionalRole = user?.role === 'employer' || user?.role === 'poslodavac' || user?.role === 'faculty' || user?.role === 'fakultet';

  return (
    <div className="form-page">
      <Header />
      <main className="form-main">
        <div className="form-container">
          <h1>Uredi profil</h1>
          {error && <div className="error-message">{error}</div>}
          {success && (
            <div style={{ 
              background: '#d1fae5', 
              border: '1px solid #86efac', 
              borderRadius: '8px', 
              padding: '1rem',
              marginBottom: '1rem',
              color: '#065f46'
            }}>
              Profil je uspješno ažuriran!
            </div>
          )}
          <form onSubmit={handleSubmit} className="form">
            {isInstitutionalRole ? (
              <div className="form-group">
                <label htmlFor="username">Korisničko ime *</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  placeholder="Korisničko ime"
                />
              </div>
            ) : (
              <>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">Ime *</label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      required
                      placeholder="Ime"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="lastName">Prezime *</label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      required
                      placeholder="Prezime"
                    />
                  </div>
                </div>
              </>
            )}

            {(user?.role === 'student' || user?.role === 'ucenik') && (
              <div className="form-group">
                <label htmlFor="faculty">Fakultet</label>
                <input
                  type="text"
                  id="faculty"
                  name="faculty"
                  value={formData.faculty}
                  onChange={handleChange}
                  placeholder="npr. FER"
                />
              </div>
            )}

            {(user?.role === 'student' || user?.role === 'ucenik') && (
              <div className="form-group">
                <label htmlFor="interestsInput">Interesi (odvojeni zarezom)</label>
                <textarea
                  id="interestsInput"
                  name="interestsInput"
                  value={formData.interestsInput}
                  onChange={handleChange}
                  rows={3}
                  placeholder="npr. programiranje, web development, AI"
                />
              </div>
            )}

            <div className="form-actions">
              <button type="button" className="btn-secondary" onClick={() => navigate('/profil')}>
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

