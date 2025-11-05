import Header from '../../components/Header';
import Footer from '../../components/Footer';
import { useNavigate } from 'react-router-dom';

export default function EmployerProfilePage() {
  const navigate = useNavigate();
  return (
    <div className="employer-profile-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Poslodavac</h1>
        <p style={{ color:'#475569' }}>Objavite oglase, istražite profile kandidata i povežite se sa zajednicom.</p>
        <div style={{ display:'flex', gap:12, flexWrap:'wrap', marginTop:16 }}>
          <button className="btn-primary" onClick={() => navigate('/prakse-i-poslovi')}>Objavi praksu/posao</button>
          <button className="btn-secondary" onClick={() => navigate('/pretraga?q=student')}>Pregled kandidata</button>
          <button className="btn-secondary" onClick={() => navigate('/resursi')}>Resursi</button>
        </div>
        <div style={{ marginTop:24, color:'#64748b' }}>
          Napomena: Napredni HR alati bit će dodani u sljedećoj fazi.
        </div>
      </main>
      <Footer />
    </div>
  );
}
