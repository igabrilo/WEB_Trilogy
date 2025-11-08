import Header from '../../components/Header';
import Footer from '../../components/Footer';
import '../../css/StaticPages.css';

export default function AboutPage() {
  return (
    <div className="static-page">
      <Header />
      <main className="static-main">
        <section className="static-hero">
          <h1>O nama</h1>
          <p>Povijest studentskog centra i UNIZG Career Hub inicijative.</p>
        </section>
        <section className="static-content">
          <article>
            <h2>Korijeni studentske podrške</h2>
            <p>
              Studentski centar u Zagrebu ima dugu tradiciju pružanja podrške studentima: od smještaja i prehrane do
              kulturnih i profesionalnih programa. UNIZG Career Hub nastavlja tu liniju – fokusiran na povezivanje
              akademskog obrazovanja i tržišta rada.
            </p>
            <p>
              Kroz godine razvijali su se programi mentora, suradnje s industrijom, međunarodne razmjene i podrška pri
              razvoju karijere. Ova platforma objedinjena je točka pristupa svim tim resursima.
            </p>
            <h2>Misija</h2>
            <p>
              Naša misija je pružiti jasne i personalizirane putanje razvoja studentima, alumnijima i poslodavcima te
              olakšati suradnju fakulteta s industrijom.
            </p>
            <h2>Vizija</h2>
            <p>
              Digitalni ekosustav koji spaja obrazovanje, praktično iskustvo i profesionalni razvoj u jedinstvenom
              sučelju dostupnom svim dionicima.
            </p>
            <div className="image-row">
              <div className="image-placeholder">Fotografija arhive</div>
              <div className="image-placeholder">Stari plakat</div>
              <div className="image-placeholder">Studentski događaj</div>
            </div>
          </article>
        </section>
      </main>
      <Footer />
    </div>
  );
}
