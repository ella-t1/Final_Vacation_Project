import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './Nav.scss';

const Nav = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleToggle = () => setMenuOpen(!menuOpen);
  const handleLinkClick = () => setMenuOpen(false);

  return (
    <nav className="nav">
      <div className="nav__logo">
        <NavLink to="/" onClick={handleLinkClick}>VacationApp</NavLink>
      </div>

      <button
        className={`nav__toggle ${menuOpen ? 'active' : ''}`}
        onClick={handleToggle}
        aria-label="Toggle menu"
      >
        <span className="bar"></span>
        <span className="bar"></span>
        <span className="bar"></span>
      </button>

      <ul className={`nav__links ${menuOpen ? 'open' : ''}`}>
        <li>
          <NavLink to="/" end onClick={handleLinkClick}>
            Home
          </NavLink>
        </li>
        <li className="nav__mobile-login">
          <NavLink to="/login" onClick={handleLinkClick}>
            Login
          </NavLink>
        </li>
        <li className="nav__mobile-login">
          <NavLink to="/signup" onClick={handleLinkClick}>
            Signup
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Nav;
