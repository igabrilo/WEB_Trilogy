import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function FacultyProfilePage() {
  const navigate = useNavigate();

  // Redirect faculty to home page (they should use their dashboard instead)
  useEffect(() => {
    navigate('/', { replace: true });
  }, [navigate]);

  return null;
}
