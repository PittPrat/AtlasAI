// Frontend: Next.js for AI-Powered Itinerary Platform

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
    const [destination, setDestination] = useState('');
    const [budget, setBudget] = useState('');
    const [interests, setInterests] = useState('');
    const [itinerary, setItinerary] = useState(null);
    const [loading, setLoading] = useState(false);

    const generateItinerary = async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:8000/generate-itinerary', {
                destination,
                budget: parseFloat(budget),
                interests: interests.split(',').map(interest => interest.trim())
            });
            setItinerary(response.data.itinerary);
        } catch (error) {
            console.error('Error generating itinerary:', error);
        }
        setLoading(false);
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
            <Image src="/logo.png" alt="AI Itinerary Logo" width={150} height={150} />

            <h1 className="text-2xl font-bold mt-4">AI-Powered Itinerary Planner</h1>
            <h1 className="text-2xl font-bold mb-4">AI-Powered Itinerary Planner</h1>
            <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
                <input
                    type="text"
                    placeholder="Enter destination"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    className="w-full p-2 mb-2 border rounded"
                />
                <input
                    type="number"
                    placeholder="Enter budget"
                    value={budget}
                    onChange={(e) => setBudget(e.target.value)}
                    className="w-full p-2 mb-2 border rounded"
                />
                <input
                    type="text"
                    placeholder="Enter interests (comma separated)"
                    value={interests}
                    onChange={(e) => setInterests(e.target.value)}
                    className="w-full p-2 mb-4 border rounded"
                />
                <button
                    onClick={generateItinerary}
                    className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                    disabled={loading}
                >
                    {loading ? 'Generating...' : 'Generate Itinerary'}
                </button>
            </div>
            {itinerary && (
                <div className="mt-6 bg-white shadow-md rounded-lg p-6 w-full max-w-md">
                    <h2 className="text-lg font-semibold mb-2">Your Itinerary:</h2>
                    <p className="text-gray-700 whitespace-pre-line">{itinerary}</p>
                </div>
            )}
        </div>
    );
}
