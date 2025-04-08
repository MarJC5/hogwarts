'use client';

import { useHouseStandings, usePointsHistory } from '@/lib/graphql';
import { useState, useEffect } from 'react';
import { 
    formatTimestamp, 
    getHouseColorWithIntensity, 
    getHouseBaseColor 
} from '@/lib/house-utils';
import Image from 'next/image'

export default function HousePoints() {
    const { loading: loadingStandings, error: standingsError, houseStandings } = useHouseStandings();
    const { loading: loadingHistory, error: historyError, pointsHistory } = usePointsHistory(undefined, 30, 10);
    const [animated, setAnimated] = useState(false);

    // Trigger animation after component mounts
    useEffect(() => {
        const timer = setTimeout(() => {
            setAnimated(true);
        }, 100);
        return () => clearTimeout(timer);
    }, []);

    if (loadingStandings || loadingHistory)
        return <p className="w-full max-w-7xl mx-auto text-center py-10">Loading house points...</p>;

    if (standingsError)
        return <p className="w-full max-w-7xl mx-auto text-center py-10 text-red-500">Error loading house standings: {standingsError.message}</p>;

    if (historyError)
        return <p className="w-full max-w-7xl mx-auto text-center py-10 text-red-500">Error loading points history: {historyError.message}</p>;

    // Sort houses by points (descending)
    const sortedHouses = [...houseStandings!].sort(
        (a, b) => b.totalPoints - a.totalPoints
    );

    // Find the highest points to calculate relative heights
    const maxPoints = Math.max(...sortedHouses.map(h => h.totalPoints), 1); // Ensure maxPoints is at least 1 to avoid division by zero

    // Calculate total points sum
    const totalPointsSum = sortedHouses.reduce((sum, house) => sum + house.totalPoints, 0);

    return (
        <div className="w-full max-w-7xl mx-auto">
            {/* House Points Visualization */}
            <div className="w-full mb-10">

                {/* Fixed-height container for points bars */}
                <div className="relative">
                    {/* House points bars container - now reversed */}
                    <div className="h-92 w-full">
                        {/* House points bars - falling from top */}
                        <div className="flex h-full w-full">
                            {sortedHouses.map(({ house, totalPoints }, index) => {
                                // Calculate height based on percentage of max points
                                const heightPercentage = (totalPoints / maxPoints) * 100;

                                // Get adjusted color based on points
                                const adjustedColor = getHouseColorWithIntensity(house, totalPoints, maxPoints);
                                const borderColor = getHouseBaseColor(house + '-border');

                                // Calculate difference from leader (if not the leader)
                                const pointDifference = index > 0 ? sortedHouses[0].totalPoints - totalPoints : 0;

                                return (
                                    <div
                                        key={house}
                                        className="w-1/4 flex flex-col md:mx-6"
                                    >
                                        <div
                                            className="w-full bar"
                                            style={{
                                                height: animated ? `${heightPercentage}%` : '0%',
                                                backgroundColor: adjustedColor,
                                                backgroundSize: 'cover',
                                                backgroundPosition: 'center',
                                                backgroundBlendMode: 'soft-light',
                                            }}
                                        >
                                            {/* House name */}
                                            <div className="text-center text-white">
                                                <h2 className="text-sm sm:text-xl mt-4">{house}</h2>
                                                <span className="text-sm">{totalPoints} pts</span>
                                                <Image 
                                                    src={`/images/${house}.png`} 
                                                    alt={house} 
                                                    width={80} 
                                                    height={80}
                                                    className="mx-auto mt-4"
                                                />
                                            </div>

                                            {/* Triangle as blason */}
                                            <div
                                                className="triangle-blason"
                                                style={{
                                                    backgroundColor: adjustedColor
                                                }}
                                            ></div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                </div>

                <div className="mb-4 text-center mt-8">Total points: {totalPointsSum}</div>
            </div>

            {/* Recent Point Changes - now using real data 
      <div className="mt-10">
        <h2 className="text-xl mb-4 font-bold">Recent Point Changes</h2>
        {pointsHistory && pointsHistory.map((entry, index) => (
          <div 
            key={index} 
            className="mb-4 p-4"
          >
            <div>
                <div className="flex justify-between">
                  <span className="font-semibold">
                    {Math.abs(entry.points)} Points {entry.isDeduction ? 'deducted from' : 'awarded to'} {entry.house}
                  </span>
                  <span className="text-sm ">
                    {formatTimestamp(entry.timestamp)}
                  </span>
                </div>
                {entry.reason && <p className="text-sm mt-1">"{entry.reason}"</p>}
                <p className="text-xs mt-1">By Professor {entry.teacher.name}</p>
              </div>
            </div>
        ))}
      </div>
      */}
        </div>
    );
}