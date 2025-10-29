import { CONSTS } from "../../consts/consts";
import "./Login.scss";
import { NavLink } from "react-router-dom";
import { useState } from "react";

const Login = () => {
  const {MAIN_TITLE, SUB_TITLE, NO_ACCOUNT, SIGNUP} = CONSTS.LOGIN;
  const [form, setForm] = useState({ email: "", password: "" });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); 
  }

  return (
    <div className="login">
      <div className="login__card">
        <h1 className="login__logo">{MAIN_TITLE}</h1>

        <form className="login__form" onSubmit={handleSubmit}>
          <input type="text" placeholder="Email" className="login__input"  onChange={(e) => {setForm({ ...form, email: e.target.value });}} value={form.email}/>
          <input
            type="password"
            placeholder="Password"
            className="login__input"
            onChange={(e) => {setForm({ ...form, password: e.target.value });}}
            value={form.password}
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
