import ClientHousePointsWrapper from './components/ClientHousePointsWrapper';

export default function Home() {
  return (
    <div className="min-h-screen">
      <header>
        <ClientHousePointsWrapper />
      </header>

      <main>
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-2">Hogwarts House Points</h1>
          <p className="text-xl text-gray-600">
            Current standings for the House Cup
          </p>
        </div>
      </main>
    </div>
  );
}
