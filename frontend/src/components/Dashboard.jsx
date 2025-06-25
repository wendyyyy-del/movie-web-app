import React, { useEffect, useState } from 'react';

const Dashboard = () => {
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUserMovies = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        setError("You must be logged in to view this page.");
        return;
      }

      try {
        const res = await fetch("http://localhost:5000/api/movies", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch movies");

        const data = await res.json();
        setMovies(data);
      } catch (err) {
        setError("Error loading your movies.");
      }
    };

    fetchUserMovies();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-3xl mb-4">🎬 Welcome to your Dashboard</h1>

      {error && <p className="text-red-500">{error}</p>}

      {movies.length === 0 && !error ? (
        <p>No movies found in your collection.</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {movies.map((movie) => (
            <div key={movie.id} className="border rounded p-2 shadow">
              <img
                src={movie.poster_url || "https://via.placeholder.com/150"}
                alt={movie.title}
                className="w-full h-48 object-cover"
              />
              <h2 className="text-lg font-semibold mt-2">{movie.title}</h2>
              <p className="text-sm text-gray-600">{movie.genre} ({movie.year})</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
