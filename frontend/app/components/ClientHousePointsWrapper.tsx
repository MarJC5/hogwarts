'use client';

import dynamic from 'next/dynamic';

// Use dynamic import with ssr: false inside a client component
const HousePoints = dynamic(() => import('./HousePoints'), {
  ssr: false,
  loading: () => <p className="w-full max-w-7xl mx-auto text-center py-10">Loading house points component...</p>
});

export default function ClientHousePointsWrapper() {
  return <HousePoints />;
} 