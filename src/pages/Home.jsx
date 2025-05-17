import React from 'react';
import { NavLink } from 'react-router-dom';
import Header from '../components/Header';

export default function Home() {
    return (
        <div>
            <Header />
            <h1>Home Page</h1>
            <p>Welcome to the homepage!</p>
            <NavLink to="/articles">Go to Articles page</NavLink>
        </div>
    );
  }