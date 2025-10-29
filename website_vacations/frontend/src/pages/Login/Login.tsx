import { CONSTS } from "../../consts/consts";
import "./Login.scss";
import { NavLink } from "react-router-dom";

const Login = () => {
  const {MAIN_TITLE, SUB_TITLE, NO_ACCOUNT, SIGNUP} = CONSTS.LOGIN;

  return (
    <div className="login">
      <div className="login__card">
        <h1 className="login__logo">{MAIN_TITLE}</h1>

        <form className="login__form">
          <input type="text" placeholder="Email" className="login__input" />
          <input
            type="password"
            placeholder="Password"
            className="login__input"
          />

          <button type="submit" className="login__button">
           {SUB_TITLE}
          </button>
        </form>
        <p className="login__signup">
          {NO_ACCOUNT}{" "}
          <NavLink to="/signup" end>
            {SIGNUP}
          </NavLink>
        </p>
      </div>
    </div>
  );
};

export default Login;
