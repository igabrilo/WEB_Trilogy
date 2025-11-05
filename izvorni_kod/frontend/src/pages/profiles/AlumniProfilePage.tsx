import { useEffect, useState } from 'react';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { apiService, type Faculty } from '../../services/api';

export default function AlumniProfilePage() {
  const [faculties, setFaculties] = useState<Faculty[]>([]);

  useEffect(() => {
    const run = async () => {
      try {
        const res = await apiService.getFaculties();
        setFaculties(res.items);
      } catch { }
    };
    run();
  }, []);

  return (
    <div className="alumni-profile-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Alumni</h1>
        <p style={{ color: '#475569' }}>Brzi kontakti fakulteta i akademija.</p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px,1fr))', gap: 16, marginTop: 16 }}>
          {faculties.map(f => (
            <div key={f.slug} className="card" style={{ padding: 14, border: '1px solid #e2e8f0', borderRadius: 8 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <div style={{ width: 36, height: 36, borderRadius: 8, background: 'var(--primary-blue)', color: '#fff', display: 'grid', placeItems: 'center', fontWeight: 700 }}>{f.abbreviation || f.name?.split(' ').map(w => w[0]).slice(0, 3).join('').toUpperCase()}</div>
                <div style={{ fontWeight: 700 }}>{f.name}</div>
              </div>
              <div style={{ display: 'grid', gap: 6 }}>
                {f.contacts?.website && (
                  <a href={f.contacts.website} target="_blank" rel="noreferrer" style={{ color: 'var(--primary-blue)', textDecoration: 'none' }}>
                    🌐 {f.contacts.website}
                  </a>
                )}
                {f.contacts?.email && (
                  <a href={`mailto:${f.contacts.email}`} style={{ color: '#0f172a', textDecoration: 'none' }}>
                    ✉️ {f.contacts.email}
                  </a>
                )}
                {f.contacts?.phone && (
                  <a href={`tel:${f.contacts.phone.replace(/\s+/g, '')}`} style={{ color: '#0f172a', textDecoration: 'none' }}>
                    📞 {f.contacts.phone}
                  </a>
                )}
                {f.contacts?.address && (
                  <div style={{ color: '#475569' }}>📍 {f.contacts.address}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
}
