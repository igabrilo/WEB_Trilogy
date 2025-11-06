import { useMemo } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import '../css/Hero.css';

type Role = 'ucenik' | 'student' | 'alumni' | 'employer' | 'faculty';

const roles: Array<{ key: Role; title: string; subtitle: string }> = [
	{ key: 'ucenik', title: 'Učenik', subtitle: 'Učenik srednje škole' },
	{ key: 'student', title: 'Student', subtitle: 'Trenutni student Sveučilišta' },
	{ key: 'alumni', title: 'Alumni', subtitle: 'Bivši student (alumnus)' },
	{ key: 'employer', title: 'Poslodavac', subtitle: 'Tvrtke i organizacije' },
	{ key: 'faculty', title: 'Fakultet', subtitle: 'Sveučilišne institucije' },
];

export default function SelectCategoryPage() {
	const navigate = useNavigate();
	const [params] = useSearchParams();
	const intent = useMemo(() => (params.get('intent') === 'register' ? 'register' : 'login'), [params]);

	const handlePick = (role: Role) => {
		if (intent === 'register') {
			navigate(`/registracija?role=${role}`);
		} else {
			navigate(`/prijava?role=${role}`);
		}
	};

	return (
		<div className="select-category-page">
			<Header />
			<main>
				<section className="profile-selection-section" style={{ paddingTop: '48px' }}>
					<div className="profile-selection-container">
						<h2 className="profile-section-title">
							{intent === 'register' ? 'Odaberite kategoriju za registraciju' : 'Odaberite kategoriju za prijavu'}
						</h2>
						<p className="profile-section-subtitle">Prilagodit ćemo iskustvo odabranom profilu</p>

									<div className="profile-grid">
							{roles.map((r) => (
								<div
									key={r.key}
												className="profile-card animate-in"
									role="button"
									tabIndex={0}
									onClick={() => handlePick(r.key)}
									onKeyDown={(e) => {
										if (e.key === 'Enter') handlePick(r.key);
									}}
								>
									<div className="profile-icon blue-icon">
										<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
											<circle cx="24" cy="24" r="10" stroke="currentColor" strokeWidth="2.5" />
										</svg>
									</div>
									<h3 className="profile-card-title">{r.title}</h3>
									<p className="profile-card-subtitle">{r.subtitle}</p>
								</div>
							))}
						</div>
					</div>
				</section>
			</main>
			<Footer />
		</div>
	);
}

