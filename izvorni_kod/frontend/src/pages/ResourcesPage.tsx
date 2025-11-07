import { useEffect, useRef } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import '../css/ResourcesPage.css';

const ResourcesPage = () => {
   const resourcesGridRef = useRef<HTMLDivElement>(null);
   const resources = [
      {
         id: 1,
         category: 'Učenje',
         title: 'Vodič za prvi posao',
         description: 'Savjeti i trikovi kako pronaći i dobiti svoj prvi posao u IT sektoru',
         type: 'Vodič',
         icon: '📚'
      },
      {
         id: 2,
         category: 'Učenje',
         title: 'Kako napisati CV',
         description: 'Kompletan vodič za izradu profesionalnog CV-a koji će privući poslodavce',
         type: 'Vodič',
         icon: '📝'
      },
      {
         id: 3,
         category: 'Učenje',
         title: 'Priprema za intervju',
         description: 'Najčešća pitanja i kako se pripremiti za uspješan intervju',
         type: 'Vodič',
         icon: '💼'
      },
      {
         id: 4,
         category: 'Alati',
         title: 'Kalkulator plaće',
         description: 'Izračunaj svoju neto plaću na temelju bruto iznosa',
         type: 'Alat',
         icon: '💰'
      },
      {
         id: 5,
         category: 'Alati',
         title: 'CV Builder',
         description: 'Kreiraj profesionalni CV pomoću našeg online alata',
         type: 'Alat',
         icon: '🛠️'
      },
      {
         id: 6,
         category: 'Mreža',
         title: 'Networking događanja',
         description: 'Pregled nadolazećih networking događanja i karijernih sajmova',
         type: 'Događaj',
         icon: '🤝'
      },
      {
         id: 7,
         category: 'Mreža',
         title: 'Mentorstvo program',
         description: 'Poveži se s iskusnim profesionalcima iz tvoje branše',
         type: 'Program',
         icon: '👨‍🏫'
      },
      {
         id: 8,
         category: 'Podrška',
         title: 'FAQ - Često postavljana pitanja',
         description: 'Odgovori na najčešća pitanja o karijeri, poslovima i studiranju',
         type: 'FAQ',
         icon: '❓'
      }
   ];

   const categories = ['Sve', 'Učenje', 'Alati', 'Mreža', 'Podrška'];

   useEffect(() => {
      const observerOptions = {
         threshold: 0.1,
         rootMargin: '0px 0px -50px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
         entries.forEach((entry) => {
            if (entry.isIntersecting) {
               entry.target.classList.add('animate-in');
            }
         });
      }, observerOptions);

      if (resourcesGridRef.current) {
         const cards = resourcesGridRef.current.querySelectorAll('.resource-card');
         cards.forEach((card, index) => {
            (card as HTMLElement).style.animationDelay = `${index * 0.1}s`;
            observer.observe(card);
         });
      }

      return () => {
         observer.disconnect();
      };
   }, []);

   return (
      <div className="resources-page">
         <Header />
         <main className="resources-main">
            <section className="resources-hero">
               <div className="resources-hero-container fade-in">
                  <h1 className="resources-hero-title slide-up">Resursi za karijeru</h1>
                  <p className="resources-hero-subtitle slide-up" style={{ animationDelay: '0.1s' }}>
                     Korisni alati, vodiči i resursi koji će ti pomoći u razvoju karijere
                  </p>
               </div>
            </section>

            <section className="resources-content">
               <div className="resources-container">
                  <div className="resources-filters slide-up" style={{ animationDelay: '0.2s' }}>
                     {categories.map(category => (
                        <button
                           key={category}
                           className={`resources-filter-btn ${category === 'Sve' ? 'active' : ''}`}
                        >
                           {category}
                        </button>
                     ))}
                  </div>

                  <div className="resources-grid" ref={resourcesGridRef}>
                     {resources.map(resource => (
                        <div key={resource.id} className="resource-card">
                           <div className="resource-icon">{resource.icon}</div>
                           <div className="resource-header">
                              <span className="resource-type">{resource.type}</span>
                              <span className="resource-category">{resource.category}</span>
                           </div>
                           <h3 className="resource-title">{resource.title}</h3>
                           <p className="resource-description">{resource.description}</p>
                           <button 
                              className="resource-btn" 
                              onClick={() => alert('Ova funkcionalnost će biti implementirana u sljedećoj fazi. Hvala na razumijevanju!')}
                           >
                              Otvori
                           </button>
                        </div>
                     ))}
                  </div>
               </div>
            </section>
         </main>
         <Footer />
      </div>
   );
};

export default ResourcesPage;

