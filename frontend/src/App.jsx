// src/App.jsx
import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import SignIn from './components/sign-in/SignIn';
import HomePage from './components/homepage';

export default function App() {
  const [userEmail, setUserEmail] = useState(null);

  return (
    <BrowserRouter>
      <Routes>
        {/* If already “logged in”, redirect /signin → / */}
        <Route
          path="/signin"
          element={
            userEmail
              ? <Navigate to="/" replace />
              : <SignIn onLogin={setUserEmail} />
          }
        />

        {/* If not logged in, redirect / → /signin */}
        <Route
          path="/"
          element={
            userEmail
              ? <HomePage userEmail={userEmail} />
              : <Navigate to="/signin" replace />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
