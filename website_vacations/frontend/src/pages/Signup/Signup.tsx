import { NavLink, useNavigate } from "react-router-dom";
import "./Signup.scss";
import { CONSTS } from "../../consts/consts";
import { useState, useEffect } from "react";
import { api } from "../../utils/api";
import { useAppDispatch } from "../../hooks/useAppDispatch";
import { useAppSelector } from "../../hooks/useAppSelector";
import { setUser } from "../../store/authSlice";

const Signup = () => {
  const {SUB_TITLE, FIRST_NAME_LABEL, LAST_NAME_LABEL, EMAIL_LABEL, PASSWORD_LABEL,BUTTON,ALREADY_MEMBER,LOGIN} = CONSTS.SIGNUP;
  const [form, setForm] = useState({ firstName: "", lastName: "", email: "", password: "" });
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setForm({ ...form, [id]: value });
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const user = await api.register({
        firstName: form.firstName,
        lastName: form.lastName,
        email: form.email,
        password: form.password,
      });
      dispatch(setUser(user));
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="signup">
      <div className="signup__card">
        <h1 className="signup__title">{SUB_TITLE}</h1>

        <form className="signup__form" onSubmit={handleSubmit}>
          {error && <div className="signup__error">{error}</div>}
          <label htmlFor="firstName">{FIRST_NAME_LABEL}</label>
          <input
            id="firstName"
            type="text"
            placeholder="First name"
            className="signup__input"
            onChange={handleChange}
            value={form.firstName}
            required
            disabled={isLoading}
          />

          <label htmlFor="lastName">{LAST_NAME_LABEL}</label>
          <input
            id="lastName"
            type="text"
            placeholder="Last name"
            className="signup__input"
            onChange={handleChange}
            value={form.lastName}
            required
            disabled={isLoading}
          />

          <label htmlFor="email">{EMAIL_LABEL}</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            className="signup__input"
            onChange={handleChange}
            value={form.email}
            required
            disabled={isLoading}
          />

          <label htmlFor="password">{PASSWORD_LABEL}</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            className="signup__input"
            onChange={handleChange}
            value={form.password}
            required
            minLength={4}
            disabled={isLoading}
          />

          <button type="submit" className="signup__button" disabled={isLoading}>
            {isLoading ? "Registering..." : BUTTON}
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
