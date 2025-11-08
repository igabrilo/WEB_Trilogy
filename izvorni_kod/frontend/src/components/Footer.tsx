import '../css/Footer.css';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface FooterLinkGroup {
   title: string;
   links: Array<{ label: string; to: string; requireAuth?: boolean; roleGate?: string | string[] }>;
}

const genericGroups: FooterLinkGroup[] = [
   {
      title: 'Kategorije',
      links: [
         { label: 'Student', to: '/prijava?role=student' },
         { label: 'Alumni', to: '/prijava?role=alumni' },
         { label: 'Učenik', to: '/prijava?role=ucenik' },
         { label: 'Poslodavac', to: '/prijava?role=employer' },
         { label: 'Fakultet', to: '/prijava?role=faculty' }
      ]
   },
   {
      title: 'Općenito',
      links: [
         { label: 'Fakulteti', to: '/fakulteti' },
         { label: 'Udruge', to: '/udruge' },
         { label: 'Prakse i poslovi', to: '/prakse-i-poslovi' },
         { label: 'Resursi', to: '/resursi' }
      ]
   }
];

const studentGroup: FooterLinkGroup = {
   title: 'Student',
   links: [
      { label: 'Pretraži poslove', to: '/prakse-i-poslovi' },
      { label: 'Udruge', to: '/udruge' },
      { label: 'Fakulteti', to: '/fakulteti' },
      { label: 'Karijerni kviz', to: '/kviz' }
   ]
};

const alumniGroup: FooterLinkGroup = {
   title: 'Alumni',
   links: [
      { label: 'Mreža Alumni', to: '/profil/alumni' },
      { label: 'Mentoriranje', to: '/profil/alumni#mentorstvo' },
      { label: 'Poslovi', to: '/prakse-i-poslovi' },
      { label: 'Dogadjanja', to: '/pretraga?q=event' }
   ]
};

const employerGroup: FooterLinkGroup = {
   title: 'Poslodavac',
   links: [
      { label: 'Objavi posao', to: '/profil/poslodavac#objava' },
      { label: 'Pretraži kandidate', to: '/profil/poslodavac#kandidati' },
      { label: 'Prakse', to: '/prakse-i-poslovi' },
      { label: 'Branding', to: '/profil/poslodavac#branding' }
   ]
};

const facultyGroup: FooterLinkGroup = {
   title: 'Fakultet',
   links: [
      { label: 'Programi', to: '/fakulteti' },
      { label: 'Udruge studenata', to: '/udruge' },
      { label: 'Erasmus projekti', to: '/pretraga?q=erasmus' },
      { label: 'Suradnje s industrijom', to: '/profil/fakultet#suradnje' }
   ]
};

const ucenikGroup: FooterLinkGroup = {
   title: 'Učenik',
   links: [
      { label: 'Istraži fakultete', to: '/fakulteti' },
      { label: 'Kviz karijere', to: '/kviz' },
      { label: 'Resursi za upis', to: '/resursi' },
      { label: 'Studentske udruge', to: '/udruge' }
   ]
};

const companyGroup: FooterLinkGroup = {
   title: 'Tvrtka',
   links: [
      { label: 'O nama', to: '/o-nama' },
      { label: 'Kontakt', to: '/kontakt' },
      { label: 'Povijest', to: '/povijest' },
      { label: 'FAQ', to: '/faq' }
   ]
};

function resolveGroups(role?: string | null): FooterLinkGroup[] {
   if (!role) {
      return [...genericGroups, companyGroup];
   }
   switch (role) {
      case 'student':
         return [studentGroup, companyGroup];
      case 'alumni':
         return [alumniGroup, companyGroup];
      case 'employer':
         return [employerGroup, companyGroup];
      case 'faculty':
         return [facultyGroup, companyGroup];
      case 'ucenik':
         return [ucenikGroup, companyGroup];
      default:
         return [...genericGroups, companyGroup];
   }
}

const Footer = () => {
   const { isAuthenticated, user } = useAuth();
   const navigate = useNavigate();
   const groups = resolveGroups(user?.role);

   const handleLink = (e: React.MouseEvent, to: string) => {
      // For unauthenticated and links that go to profile-specific screens, redirect to login with inferred role
      if (!isAuthenticated && to.startsWith('/profil/')) {
         e.preventDefault();
         // infer role from url part
         const part = to.split('/')[2];
         navigate(`/prijava?role=${encodeURIComponent(part)}`);
         return;
      }
   };

   return (
      <footer className="footer">
         <div className="footer-container">
            <div className="footer-content">
               <div className="footer-column">
                  <h3 className="footer-title">UNIZG Career Hub</h3>
                  <p className="footer-description">
                     Povezujemo studente i alumni Sveučilišta u Zagrebu s poslodavcima i poslovnim prilikama.
                  </p>
                  <div className="social-links">
                     <a href="#" className="social-link" aria-label="Facebook">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" /></svg>
                     </a>
                     <a href="#" className="social-link" aria-label="Twitter">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" /></svg>
                     </a>
                     <a href="#" className="social-link" aria-label="LinkedIn">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" /></svg>
                     </a>
                  </div>
               </div>
               {groups.map(group => (
                  <div className="footer-column" key={group.title}>
                     <h4 className="footer-heading">{group.title}</h4>
                     <ul className="footer-links">
                        {group.links.map(link => (
                           <li key={link.label}>
                              <Link to={link.to} onClick={(e) => handleLink(e, link.to)}>{link.label}</Link>
                           </li>
                        ))}
                     </ul>
                  </div>
               ))}
            </div>
            <div className="footer-bottom">
               <p>&copy; 2025 UNIZG Career Hub. Sva prava pridržana.</p>
            </div>
         </div>
      </footer>
   );
};

export default Footer;
