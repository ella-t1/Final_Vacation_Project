import { NavLink } from "react-router-dom";
import "./Signup.scss";
import { CONSTS } from "../../consts/consts";
import { useState } from "react";

const Signup = () => {
  const {SUB_TITLE, FIRST_NAME_LABEL, LAST_NAME_LABEL, EMAIL_LABEL, PASSWORD_LABEL,BUTTON,ALREADY_MEMBER,LOGIN} = CONSTS.SIGNUP;
  const [form, setForm] = useState({ firstName: "", lastName: "", email: "", password: "" });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setForm({ ...form, [id]: value });
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); 
    console.log(form)
  }

  return (
    <div className="signup">
      <div className="signup__card">
        <h1 className="signup__title">{SUB_TITLE}</h1>

        <form className="signup__form" onSubmit={handleSubmit}>
          <label htmlFor="firstName">{FIRST_NAME_LABEL}</label>
          <input
            id="firstName"
            type="text"
            placeholder="First name"
            className="signup__input"
            onChange={handleChange}
            value={form.firstName}
          />

          <label htmlFor="lastName">{LAST_NAME_LABEL}</label>
          <input
            id="lastName"
            type="text"
            placeholder="Last name"
            className="signup__input"
            onChange={handleChange}
            value={form.lastName}
          />

          <label htmlFor="email">{EMAIL_LABEL}</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            className="signup__input"
            onChange={handleChange}
            value={form.email}
          />

          <label htmlFor="password">{PASSWORD_LABEL}</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            className="signup__input"
            onChange={handleChange}
            value={form.password}
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
