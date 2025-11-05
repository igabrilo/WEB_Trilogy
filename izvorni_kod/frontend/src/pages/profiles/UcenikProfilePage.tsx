import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useNavigate } from 'react-router-dom';

export default function UcenikProfilePage() {
  const navigate = useNavigate();
  return (
    <div className="ucenik-profile-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Učenik</h1>
        <p style={{ color:'#475569' }}>Istraži fakultete i pripremi se za odabir studija.</p>
        <div style={{ display:'flex', gap:12, flexWrap:'wrap', marginTop:16 }}>
          <button className="btn-primary" onClick={() => navigate('/fakulteti')}>Istraži fakultete</button>
          <button className="btn-secondary" onClick={() => navigate('/kviz')}>Kviz profesionalne orijentacije</button>
          <button className="btn-secondary" onClick={() => navigate('/resursi')}>Korisni resursi</button>
        </div>
        <section style={{ marginTop:28 }}>
          <h2>Što te očekuje u kvizu?</h2>
          <ul style={{ marginTop:8, color:'#475569' }}>
            <li>Pitanja o interesima i vještinama</li>
            <li>Prijedlozi područja i studija</li>
            <li>Savjeti za upis i pripremu</li>
          </ul>
        </section>
      </main>
      <Footer />
    </div>
  );
}
