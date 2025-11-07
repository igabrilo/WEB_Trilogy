import Header from '../../components/Header';
import Footer from '../../components/Footer';
import '../../css/StaticPages.css';

export default function ContactPage() {
  return (
    <div className="static-page">
      <Header />
      <main className="static-main">
        <section className="static-hero">
          <h1>Kontakt</h1>
          <p>Kontakt Studentskog centra / Career Hub tima</p>
        </section>
        <section className="static-content">
          <div className="contact-card">
            <div className="contact-row">
              <span className="contact-label">Adresa</span>
              <span className="contact-value">Savska cesta 25, 10000 Zagreb</span>
            </div>
            <div className="contact-row">
              <span className="contact-label">E-mail</span>
              <a className="contact-value" href="mailto:info@sczg.hr">info@sczg.hr</a>
            </div>
            <div className="contact-row">
              <span className="contact-label">Telefon</span>
              <a className="contact-value" href="tel:+38516009000">+385 1 6009 000</a>
            </div>
            <div className="contact-row">
              <span className="contact-label">Radno vrijeme</span>
              <span className="contact-value">Pon–Pet: 08:00–16:00</span>
            </div>
            <div className="logo-slot">LOGO / GRB</div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}
