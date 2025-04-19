import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import SignIn from './components/sign-in/SignIn';
import HomePage from './components/homepage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Home page at “/” */}
        <Route path="/" element={<HomePage />} />
        {/* Sign‑in page at “/signin” */}
        <Route path="/signin" element={<SignIn />} />
      </Routes>
    </BrowserRouter>
  );
}
