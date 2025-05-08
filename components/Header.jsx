import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Header() {
    return (
      <header>
        <nav>
          <ul>
            <li>
              <NavLink to="/">Home</NavLink>
            </li>
            <li>
              <NavLink to="/about">About</NavLink>
            </li>
            <li>
              <NavLink to="/articles">Articles</NavLink>
            </li>
          </ul>
        </nav>
      </header>
    );
  }