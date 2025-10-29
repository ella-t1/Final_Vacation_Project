import { NavLink } from "react-router-dom";
import "./Signup.scss";
import { CONSTS } from "../../consts/consts";

const Signup = () => {
  const {SUB_TITLE, FIRST_NAME_LABEL, LAST_NAME_LABEL, EMAIL_LABEL, PASSWORD_LABEL,BUTTON,ALREADY_MEMBER,LOGIN} = CONSTS.SIGNUP;

  return (
    <div className="signup">
      <div className="signup__card">
        <h1 className="signup__title">{SUB_TITLE}</h1>

        <form className="signup__form">
          <label htmlFor="firstName">{FIRST_NAME_LABEL}</label>
          <input
            id="firstName"
            type="text"
            placeholder="First name"
            className="signup__input"
          />

          <label htmlFor="lastName">{LAST_NAME_LABEL}</label>
          <input
            id="lastName"
            type="text"
            placeholder="Last name"
            className="signup__input"
          />

          <label htmlFor="email">{EMAIL_LABEL}</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            className="signup__input"
          />

          <label htmlFor="password">{PASSWORD_LABEL}</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            className="signup__input"
          />

          <button type="submit" className="signup__button">
            {BUTTON}
          </button>
        </form>

        <p className="signup__login">
          {ALREADY_MEMBER}{" "}
          <NavLink to="/login" end>
            {LOGIN}
          </NavLink>
        </p>
      </div>
    </div>
  );
};

export default Signup;
