import { CONSTS } from "../../consts/consts";
import "./Login.scss";
import { NavLink, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { api } from "../../utils/api";
import { useAppDispatch } from "../../hooks/useAppDispatch";
import { useAppSelector } from "../../hooks/useAppSelector";
import { setUser } from "../../store/authSlice";

const Login = () => {
  const {MAIN_TITLE, SUB_TITLE, NO_ACCOUNT, SIGNUP} = CONSTS.LOGIN;
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.auth.user);

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const user = await api.login({
        email: form.email,
        password: form.password,
      });
      dispatch(setUser(user));
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="login">
      <div className="login__card">
        <h1 className="login__logo">{MAIN_TITLE}</h1>

        <form className="login__form" onSubmit={handleSubmit}>
          {error && <div className="login__error">{error}</div>}
          <input 
            type="email" 
            placeholder="Email" 
            className="login__input"  
            onChange={(e) => {setForm({ ...form, email: e.target.value });}} 
            value={form.email}
            required
            disabled={isLoading}
          />
          <input
            type="password"
            placeholder="Password"
            className="login__input"
            onChange={(e) => {setForm({ ...form, password: e.target.value });}}
            value={form.password}
            required
            disabled={isLoading}
          />

          <button type="submit" className="login__button" disabled={isLoading}>
           {isLoading ? "Logging in..." : SUB_TITLE}
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
