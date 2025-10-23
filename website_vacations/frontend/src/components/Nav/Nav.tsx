import React, { useState } from 'react';
import './Nav.scss';

const Nav = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="nav">
      <div className="nav__logo">VacationApp</div>

      <button 
        className={`nav__toggle ${menuOpen ? 'active' : ''}`} 
        onClick={() => setMenuOpen(!menuOpen)}
        aria-label="Toggle menu"
      >
        <span className="bar"></span>
        <span className="bar"></span>
        <span className="bar"></span>
      </button>

      <ul className={`nav__links ${menuOpen ? 'open' : ''}`}>
        <li><a href="/">Home</a></li>
        <li><a href="/destinations">Destinations</a></li>
        <li><a href="/about">About</a></li>
        <li className="nav__mobile-login"><a href="/login">Login</a></li>
      </ul>

      <button className="nav__login">Login</button>
    </nav>
  );
};

export default Nav;
