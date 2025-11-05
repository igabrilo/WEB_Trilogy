import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import '../css/ProfilePage.css';

const ProfilePage = () => {
   const { user } = useAuth();
   const [activeTab, setActiveTab] = useState('overview');

   return (
      <div className="profile-page">
         <Header />
         <main className="profile-main">
            <section className="profile-hero">
               <div className="profile-hero-container">
                  <div className="profile-avatar">
                     <div className="avatar-circle">
                        <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                           <circle cx="32" cy="24" r="12" stroke="currentColor" strokeWidth="2.5" />
                           <path d="M16 56c0-8.8 7.2-16 16-16s16 7.2 16 16" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
                        </svg>
                     </div>
                     <button className="edit-avatar-btn">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                           <path d="M11.5 2.5l2 2M1 15l3.5-3.5L11 13l-2-2-3.5-3.5L1 8v7z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                     </button>
                  </div>
                  <div className="profile-info">
                     <h1 className="profile-name">
                        {user ? `${user.firstName} ${user.lastName}` : 'Ime Prezime'}
                     </h1>
                     <p className="profile-role">
                        {user ? `${user.role.charAt(0).toUpperCase() + user.role.slice(1)}` : 'Student'}{user?.faculty ? ` - ${user.faculty}` : ''}
                     </p>
                     <p className="profile-email">
                        {user?.email || 'ime.prezime@student.fer.hr'}
                     </p>
                  </div>
                  <button className="profile-edit-btn">Uredi profil</button>
               </div>
            </section>

            <section className="profile-content">
               <div className="profile-container">
                  <div className="profile-tabs">
                     <button
                        className={`profile-tab ${activeTab === 'overview' ? 'active' : ''}`}
                        onClick={() => setActiveTab('overview')}
                     >
                        Pregled
                     </button>
                     <button
                        className={`profile-tab ${activeTab === 'experience' ? 'active' : ''}`}
                        onClick={() => setActiveTab('experience')}
                     >
                        Iskustvo
                     </button>
                     <button
                        className={`profile-tab ${activeTab === 'education' ? 'active' : ''}`}
                        onClick={() => setActiveTab('education')}
                     >
                        Obrazovanje
                     </button>
                     <button
                        className={`profile-tab ${activeTab === 'applications' ? 'active' : ''}`}
                        onClick={() => setActiveTab('applications')}
                     >
                        Prijave
                     </button>
                  </div>

                  <div className="profile-tab-content">
                     {activeTab === 'overview' && (
                        <div className="overview-content">
                           <div className="profile-card">
                              <h3 className="profile-card-title">O meni</h3>
                              <p className="profile-card-text">
                                 Student sam Fakulteta elektrotehnike i računarstva, zainteresiran za
                                 software development i web tehnologije. Tražim priliku za praksu
                                 ili part-time posao u IT sektoru.
                              </p>
                           </div>
                           <div className="profile-card">
                              <h3 className="profile-card-title">Vještine</h3>
                              <div className="skills-list">
                                 <span className="skill-tag">JavaScript</span>
                                 <span className="skill-tag">React</span>
                                 <span className="skill-tag">TypeScript</span>
                                 <span className="skill-tag">Python</span>
                                 <span className="skill-tag">Java</span>
                                 <span className="skill-tag">Git</span>
                              </div>
                           </div>
                           <div className="profile-card">
                              <h3 className="profile-card-title">Statistika</h3>
                              <div className="stats-grid">
                                 <div className="stat-item">
                                    <div className="stat-value">12</div>
                                    <div className="stat-label">Prijavljenih oglasa</div>
                                 </div>
                                 <div className="stat-item">
                                    <div className="stat-value">5</div>
                                    <div className="stat-label">Aktivnih prijava</div>
                                 </div>
                                 <div className="stat-item">
                                    <div className="stat-value">2</div>
                                    <div className="stat-label">Intervjua</div>
                                 </div>
                              </div>
                           </div>
                        </div>
                     )}

                     {activeTab === 'experience' && (
                        <div className="experience-content">
                           <div className="profile-card">
                              <h3 className="profile-card-title">Radno iskustvo</h3>
                              <div className="experience-list">
                                 <div className="experience-item">
                                    <div className="experience-header">
                                       <h4 className="experience-title">Junior Developer</h4>
                                       <span className="experience-period">2023 - Sada</span>
                                    </div>
                                    <p className="experience-company">Tech Startup</p>
                                    <p className="experience-description">
                                       Razvoj web aplikacija koristeći React i Node.js
                                    </p>
                                 </div>
                              </div>
                           </div>
                        </div>
                     )}

                     {activeTab === 'education' && (
                        <div className="education-content">
                           <div className="profile-card">
                              <h3 className="profile-card-title">Obrazovanje</h3>
                              <div className="education-list">
                                 <div className="education-item">
                                    <div className="education-header">
                                       <h4 className="education-title">Fakultet elektrotehnike i računarstva</h4>
                                       <span className="education-period">2021 - Sada</span>
                                    </div>
                                    <p className="education-degree">Preddiplomski studij - Računarstvo</p>
                                    <p className="education-gpa">Prosjek: 4.2</p>
                                 </div>
                              </div>
                           </div>
                        </div>
                     )}

                     {activeTab === 'applications' && (
                        <div className="applications-content">
                           <div className="profile-card">
                              <h3 className="profile-card-title">Moje prijave</h3>
                              <div className="applications-list">
                                 <div className="application-item">
                                    <div className="application-header">
                                       <h4 className="application-title">Software Engineer - Tech Corp</h4>
                                       <span className="application-status pending">U procesu</span>
                                    </div>
                                    <p className="application-date">Prijavljeno: 15. studenog 2024.</p>
                                 </div>
                                 <div className="application-item">
                                    <div className="application-header">
                                       <h4 className="application-title">Ljetna praksa - Digital Agency</h4>
                                       <span className="application-status accepted">Prihvaćeno</span>
                                    </div>
                                    <p className="application-date">Prijavljeno: 10. studenog 2024.</p>
                                 </div>
                              </div>
                           </div>
                        </div>
                     )}
                  </div>
               </div>
            </section>
         </main>
         <Footer />
      </div>
   );
};

export default ProfilePage;

