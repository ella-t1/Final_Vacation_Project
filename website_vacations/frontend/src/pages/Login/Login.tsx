import "./Login.scss";
import { NavLink } from "react-router-dom";

const Login = () => {
  return (
    <div className="login">
      <div className="login__card">
        <h1 className="login__logo">VacationApp</h1>

        <form className="login__form">
          <input type="text" placeholder="Email" className="login__input" />
          <input
            type="password"
            placeholder="Password"
            className="login__input"
          />

          <button type="submit" className="login__button">
            Log In
          </button>
        </form>
        <p className="login__signup">
          Don’t have an account?{" "}
          <NavLink to="/signup" end>
            Signup
          </NavLink>
        </p>
      </div>
    </div>
  );
};

export default Login;
