import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useNavigate } from 'react-router-dom';

export default function FacultyProfilePage() {
  const navigate = useNavigate();
  return (
    <div className="faculty-profile-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Fakultet / Akademija</h1>
        <p style={{ color:'#475569' }}>Promovirajte programe i povežite se sa studentima i alumnijima.</p>
        <div style={{ display:'flex', gap:12, flexWrap:'wrap', marginTop:16 }}>
          <button className="btn-primary" onClick={() => navigate('/fakulteti')}>Pregled svih sastavnica</button>
          <button className="btn-secondary" onClick={() => navigate('/pretraga?q=udruga')}>Studentske udruge</button>
          <button className="btn-secondary" onClick={() => navigate('/resursi')}>Resursi</button>
        </div>
        <div style={{ marginTop:24, color:'#64748b' }}>
          Napomena: Upravljačka sučelja za sastavnice bit će dodana u sljedećoj fazi.
        </div>
      </main>
      <Footer />
    </div>
  );
}
