import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../css/FeaturedJobs.css';

interface Job {
   id: number;
   title: string;
   company: string;
   location: string;
   type: string;
   salary: string;
   posted: string;
   logo: string;
}

const FeaturedJobs = () => {
   const { isAuthenticated } = useAuth();
   const navigate = useNavigate();
   const jobs: Job[] = [
      {
         id: 1,
         title: "Software Engineer",
         company: "Tech Corp",
         location: "Zagreb, Hrvatska",
         type: "Puno radno vrijeme",
         salary: "€40,000 - €60,000",
         posted: "prije 2 dana",
         logo: "TC"
      },
      {
         id: 2,
         title: "Data Analyst",
         company: "Data Solutions",
         location: "Udaljeno",
         type: "Puno radno vrijeme",
         salary: "€35,000 - €50,000",
         posted: "prije 3 dana",
         logo: "DS"
      },
      {
         id: 3,
         title: "UX Designer",
         company: "Design Studio",
         location: "Zagreb, Hrvatska",
         type: "Djelomično radno vrijeme",
         salary: "€30,000 - €45,000",
         posted: "prije 1 tjedan",
         logo: "DS"
      },
      {
         id: 4,
         title: "Marketing Manager",
         company: "Growth Co",
         location: "Split, Hrvatska",
         type: "Puno radno vrijeme",
         salary: "€35,000 - €55,000",
         posted: "prije 5 dana",
         logo: "GC"
      }
   ];

   return (
      <section className="featured-jobs">
         <div className="container">
            <div className="section-header">
               <h2 className="section-title">Istaknute prilike za posao</h2>
               <p className="section-description">
                  Istraži najnovije otvorene pozicije od vodećih tvrtki
               </p>
            </div>
            <div className="jobs-grid">
               {jobs.map(job => (
                  <div key={job.id} className="job-card">
                     <div className="job-header">
                        <div className="company-logo">{job.logo}</div>
                        <span className="job-type">{job.type}</span>
                     </div>
                     <h3 className="job-title">{job.title}</h3>
                     <p className="company-name">{job.company}</p>
                     <div className="job-details">
                        <div className="job-detail">
                           <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                              <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                              <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                           </svg>
                           <span>{job.location}</span>
                        </div>
                        <div className="job-detail">
                           <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                              <path d="M8 1v7l4 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                              <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" />
                           </svg>
                           <span>{job.posted}</span>
                        </div>
                     </div>
                     <div className="job-salary">{job.salary}</div>
                     <button 
                        className="job-apply-btn"
                        onClick={() => {
                           if (isAuthenticated) {
                              // TODO: Implementiraj prijavu na posao
                              alert('Funkcija prijave će biti implementirana');
                           } else {
                              navigate('/prijava');
                           }
                        }}
                     >
                        {isAuthenticated ? 'Prijavi se' : 'Prijavi se (zahtijeva prijavu)'}
                     </button>
                  </div>
               ))}
            </div>
            <div className="view-all">
               <button className="btn-view-all">Prikaži sve poslove</button>
            </div>
         </div>
      </section>
   );
};

export default FeaturedJobs;
