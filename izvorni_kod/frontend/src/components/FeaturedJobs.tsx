import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService, type Job } from '../services/api';
import '../css/FeaturedJobs.css';

const FeaturedJobs = () => {
   const { isAuthenticated } = useAuth();
   const navigate = useNavigate();
   const [jobs, setJobs] = useState<Job[]>([]);
   const [loading, setLoading] = useState(true);

   useEffect(() => {
      const loadJobs = async () => {
         try {
            const res = await apiService.getJobs({ type: 'job' });
            setJobs(res.items.slice(0, 4)); // Show only first 4 featured jobs
         } catch (error) {
            console.error('Error loading jobs:', error);
         } finally {
            setLoading(false);
         }
      };
      loadJobs();
   }, []);

   return (
      <section className="featured-jobs">
         <div className="container">
            <div className="section-header">
               <h2 className="section-title">Istaknute prilike za posao</h2>
               <p className="section-description">
                  Istraži najnovije otvorene pozicije od vodećih tvrtki
               </p>
            </div>
            {loading ? (
               <div style={{ padding: '2rem', textAlign: 'center' }}>Učitavanje poslova...</div>
            ) : jobs.length === 0 ? (
               <div style={{ padding: '2rem', textAlign: 'center' }}>Trenutno nema dostupnih poslova.</div>
            ) : (
               <div className="jobs-grid">
                  {jobs.map(job => {
                     const logoText = job.company ? job.company.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase() : 'CO';
                     const typeLabel = job.type === 'internship' ? 'Praksa' :
                        job.type === 'job' ? 'Puno radno vrijeme' :
                           job.type === 'part-time' ? 'Djelomično radno vrijeme' :
                              job.type === 'remote' ? 'Udaljeno' : job.type;

                     return (
                        <div key={job.id} className="job-card">
                           <div className="job-header">
                              <div className="company-logo">{logoText}</div>
                              <span className="job-type">{typeLabel}</span>
                           </div>
                           <h3 className="job-title">{job.title}</h3>
                           {job.company && <p className="company-name">{job.company}</p>}
                           <div className="job-details">
                              {job.location && (
                                 <div className="job-detail">
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                       <path d="M8 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" stroke="currentColor" strokeWidth="1.5" />
                                       <path d="M8 1c-3 0-5.5 2.5-5.5 5.5 0 4 5.5 8.5 5.5 8.5s5.5-4.5 5.5-8.5C13.5 3.5 11 1 8 1z" stroke="currentColor" strokeWidth="1.5" />
                                    </svg>
                                    <span>{job.location}</span>
                                 </div>
                              )}
                              {job.createdAt && (
                                 <div className="job-detail">
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                       <path d="M8 1v7l4 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                       <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" />
                                    </svg>
                                    <span>{new Date(job.createdAt).toLocaleDateString('hr-HR')}</span>
                                 </div>
                              )}
                           </div>
                           {job.salary && <div className="job-salary">{job.salary}</div>}
                           <button
                              className="job-apply-btn"
                              onClick={() => {
                                 if (isAuthenticated) {
                                    navigate(`/prakse-i-poslovi/${job.id}`);
                                 } else {
                                    navigate('/prijava');
                                 }
                              }}
                           >
                              {isAuthenticated ? 'Prijavi se' : 'Prijavi se (zahtijeva prijavu)'}
                           </button>
                        </div>
                     );
                  })}
               </div>
            )}
            {jobs.length > 0 && (
               <div className="view-all">
                  <button className="btn-view-all" onClick={() => navigate('/prakse-i-poslovi')}>
                     Prikaži sve poslove
                  </button>
               </div>
            )}
         </div>
      </section>
   );
};

export default FeaturedJobs;
