import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

export default function ArticlesList() {
  const [articles, setArticles] = useState([]);
  
    useEffect(() => {
      // Fetch the CSV file from the public folder
      fetch('/articles/articles.csv')
        .then(response => response.text())
        .then(csvText => {
          const parsed = Papa.parse(csvText, { header: true });
          setArticles(parsed.data);
        })
        .catch(error => {
          console.error('Error loading CSV:', error);
        });
    }, []);
  
  return articles
}

