import Header from '../../components/Header';
import Footer from '../../components/Footer';
import '../../css/StaticPages.css';

export default function FAQPage() {
  return (
    <div className="static-page">
      <Header />
      <main className="static-main">
        <section className="static-hero">
          <h1>Česta pitanja (FAQ)</h1>
          <p>Brzi odgovori na najčešća pitanja o korištenju platforme.</p>
        </section>
        <section className="static-content">
          <article>
            <h2>Prijava i registracija</h2>
            <ul>
              <li><strong>Kako odabrati profil?</strong> Na prijavi/registraciji odaberite profil (Student, Alumni, Učenik, Poslodavac, Fakultet) i nastavite s obrascem.</li>
              <li><strong>Zaboravljena lozinka?</strong> Kliknite na "Zaboravili ste lozinku?" na ekranu prijave.</li>
            </ul>
            <h2>Studenti</h2>
            <ul>
              <li><strong>Gdje tražim poslove?</strong> Na stranici "Prakse i poslovi" ili kroz preporuke na vašoj profilnoj stranici.</li>
              <li><strong>Kako urediti profil?</strong> Nakon prijave, otvorite "Profil" → "Uredi profil".</li>
            </ul>
            <h2>Poslodavci</h2>
            <ul>
              <li><strong>Kako objaviti posao?</strong> Na profilu poslodavca otvorite sekciju "Objavi posao".</li>
              <li><strong>Kako filtrirati kandidate?</strong> U sekciji "Pretraži kandidate" dostupni su filteri po vještinama, fakultetu i iskustvu.</li>
            </ul>
            <h2>Kontakt</h2>
            <p>Za dodatna pitanja, posjetite stranicu <a href="/kontakt">Kontakt</a>.</p>
          </article>
        </section>
      </main>
      <Footer />
    </div>
  );
}
