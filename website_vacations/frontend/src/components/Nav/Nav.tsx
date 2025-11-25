import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import "./Nav.scss";
import { CONSTS } from "../../consts/consts";
import { useAppSelector } from "../../hooks/useAppSelector";
import { useAppDispatch } from "../../hooks/useAppDispatch";
import { clearUser } from "../../store/authSlice";

const Nav = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const {LOGO, HOME, LOGIN, SIGNUP, TOGGLE_ARIA} = CONSTS.NAVBAR;
  const user = useAppSelector((state) => state.auth.user);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const handleToggle = () => setMenuOpen(!menuOpen);
  const handleLinkClick = () => setMenuOpen(false);
  
  const handleLogout = () => {
    dispatch(clearUser());
    localStorage.removeItem("auth_user"); // Ensure localStorage is cleared
    navigate("/");
    setMenuOpen(false);
  };

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
        {user ? (
          <>
            {user.roleId === 1 && (
              <li>
                <NavLink to="/create-vacation" onClick={handleLinkClick}>
                  Add Vacation
                </NavLink>
              </li>
            )}
            <li>
              <span className="nav__user">
                {user.firstName} {user.lastName}
              </span>
            </li>
            <li className="nav__mobile-login">
              <button onClick={handleLogout} className="nav__logout">
                Logout
              </button>
            </li>
          </>
        ) : (
          <>
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
          </>
        )}
      </ul>
    </nav>
  );
};

export default Nav;
