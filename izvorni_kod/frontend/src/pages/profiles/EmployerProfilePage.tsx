import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function EmployerProfilePage() {
  const navigate = useNavigate();

  // Redirect employer to home page (they should use their dashboard instead)
  useEffect(() => {
    navigate('/', { replace: true });
  }, [navigate]);

  return null;
}
