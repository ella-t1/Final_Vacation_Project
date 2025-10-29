import { useState } from "react";
import { NavLink } from "react-router-dom";
import "./Nav.scss";
import { CONSTS } from "../../consts/consts";

const Nav = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const {LOGO, HOME, LOGIN, SIGNUP, TOGGLE_ARIA} = CONSTS.NAVBAR;

  const handleToggle = () => setMenuOpen(!menuOpen);
  const handleLinkClick = () => setMenuOpen(false);

  return (
    <nav className="nav">
      <div className="nav__logo">
        <NavLink to="/" onClick={handleLinkClick}>
          {LOGO}
        </NavLink>
      </div>

      <button
        className={`nav__toggle ${menuOpen ? "active" : ""}`}
        onClick={handleToggle}
        aria-label={TOGGLE_ARIA}
      >
        <span className="bar"></span>
        <span className="bar"></span>
        <span className="bar"></span>
      </button>

      <ul className={`nav__links ${menuOpen ? "open" : ""}`}>
        <li>
          <NavLink to="/" end onClick={handleLinkClick}>
            {HOME}
          </NavLink>
        </li>
        <li className="nav__mobile-login">
          <NavLink to="/login" onClick={handleLinkClick}>
            {LOGIN}
          </NavLink>
        </li>
        <li className="nav__mobile-login">
          <NavLink to="/signup" onClick={handleLinkClick}>
            {SIGNUP}
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Nav;
