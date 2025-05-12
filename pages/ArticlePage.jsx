import React from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/Header';
import ArticlesList from '../pages/ArticlesList';
import parse from 'html-react-parser';


export default function ArticlePage() {
    const { slug } = useParams();
    const articles = ArticlesList();

    const article = articles.find(a => a.article_weblink === slug);

    if (!article) return <div>Loading or not found...</div>; {/*to be filled*/}

    return (
        <div>
            <Header />
            <h1>{article.article_name}</h1>
            <p>by {article.author}</p>
            <p>{article.date}</p>
           {/*main body*/} 
           <p>{parse(article.content)}</p> 
        </div>
    );
  }