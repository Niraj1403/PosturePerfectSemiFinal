import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

// Import Pages
import Home from "./pages/Home/Home";
import Yoga from "./pages/Yoga/Yoga";
import HowItWorks from "./pages/About/HowItWorks";
import Signup from "./pages/Tutorials/Signup";
import SuryaNamaskar from "./pages/Yoga/SuryaNamaskar"; // ✅ New Surya Namaskar Page

// Import Navbar
import Navbar from "./Navbar"; // ✅ Navbar is directly in src/

// Import CSS
import "./App.css";

export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/start" element={<Yoga />} />
        <Route path="/howitworks" element={<HowItWorks />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/surya-namaskar" element={<SuryaNamaskar />} /> {/* ✅ New Route */}
      </Routes>
    </Router>
  );
}