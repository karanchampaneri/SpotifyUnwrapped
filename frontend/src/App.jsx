import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <main className="w-screen h-screen bg-white text-black flex flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-2 text-green-500">
        Spotify Unwrapped
      </h1>
      <p className="text-gray-700 mb-4 text-center">
        An app that knows you love sad girl anthems at 2 AM.
      </p>
      <button
        className="px-4 py-2 bg-emerald-600 text-white font-semibold rounded hover:bg-emerald-500 transition"
        onClick={() => setCount(count + 1)}
      >
        Clicked {count} times
      </button>
    </main>
  );
}
