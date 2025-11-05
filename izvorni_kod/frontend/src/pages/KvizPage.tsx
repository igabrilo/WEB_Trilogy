import Header from '../components/Header';
import Footer from '../components/Footer';

export default function KvizPage() {
  return (
    <div className="kviz-page">
      <Header />
      <main className="container" style={{ padding: '2rem 1rem' }}>
        <h1>Kviz profesionalne orijentacije</h1>
        <p style={{ color:'#475569' }}>U izradi. Ovdje ćeš uskoro moći ispuniti kviz i dobiti prijedloge studija.</p>
      </main>
      <Footer />
    </div>
  );
}
