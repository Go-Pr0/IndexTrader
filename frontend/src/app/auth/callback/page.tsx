'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const AuthCallbackPage = () => {
  const router = useRouter();

  useEffect(() => {
    // Here you would typically handle the auth callback,
    // exchange the code for a token, and then redirect.
    // For now, we'll just redirect to the dashboard.
    router.push('/dashboard');
  }, [router]);

  return (
    <div>
      <h1>Loading...</h1>
      <p>Please wait while we log you in.</p>
    </div>
  );
};

export default AuthCallbackPage;
