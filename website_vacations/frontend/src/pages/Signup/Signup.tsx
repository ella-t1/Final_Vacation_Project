import { NavLink } from "react-router-dom";
import "./Signup.scss";

const Signup = () => {
  return (
    <div className="signup">
      <div className="signup__card">
        <h1 className="signup__title">Register</h1>

        <form className="signup__form">
          <label htmlFor="firstName">first name</label>
          <input
            id="firstName"
            type="text"
            placeholder="First name"
            className="signup__input"
          />

          <label htmlFor="lastName">last name</label>
          <input
            id="lastName"
            type="text"
            placeholder="Last name"
            className="signup__input"
          />

          <label htmlFor="email">email</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            className="signup__input"
          />

          <label htmlFor="password">password</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            className="signup__input"
          />

          <button type="submit" className="signup__button">
            Register
          </button>
        </form>

        <p className="signup__login">
          already a member?{" "}
          <NavLink to="/login" end>
            Login
          </NavLink>
        </p>
      </div>
    </div>
  );
};

export default Signup;
