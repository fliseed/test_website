import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Papa from 'papaparse';

export default function Articles() {
    const [articles, setArticles] = useState([]);
  
    useEffect(() => {
      // Fetch the CSV file from the public folder
      fetch('/pages/articles/articles.csv')
        .then(response => response.text())
        .then(csvText => {
          const parsed = Papa.parse(csvText, { header: true });
          setArticles(parsed.data);
        })
        .catch(error => {
          console.error('Error loading CSV:', error);
        });
    }, []);
    console.log(articles);
  
    return (
      <div>
        <Header />
        <h1>Article Page</h1>
        <p>Welcome to the articles!</p>
        <p>Here you can find a list of articles.</p>
  
        <ul>
          {articles.map((article, index) => (
            <li key={index}>
              {article.article_name} by {article.author}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  