import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import Articles from './pages/Articles';
import Papa from 'papaparse';
import ArticlePage from './pages/ArticlePage';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path = "articles" element={<Articles />} />
        <Route path = "articles/:slug" element={<ArticlePage />} />
      </Routes>
    </Router>
  );
}

export default App;
