import { CONSTS } from "../../consts/consts";
import "./CreateVacation.scss";
import { useState, useEffect } from "react";
import { api, Country } from "../../utils/api";
import { useNavigate } from "react-router-dom";
import { useAppSelector } from "../../hooks/useAppSelector";

interface VacationForm {
  country: string;
  description: string;
  startDate: string;
  endDate: string;
  price: string;
  image: File | null;
}

const CreateVacation = () => {
  const {
    TITLE,
    COUNTRY_LABEL,
    COUNTRY_PLACEHOLDER,
    DESCRIPTION_LABEL,
    DESCRIPTION_PLACEHOLDER,
    START_LABEL,
    END_LABEL,
    PRICE_LABEL,
    PRICE_PLACEHOLDER,
    CURRENCY_SYMBOL,
    COVER_LABEL,
    SELECT_IMAGE,
    ADD_BUTTON,
    CANCEL_BUTTON,
  } = CONSTS.CREATE_VACATIONS;

  const user = useAppSelector((state) => state.auth.user);
  const navigate = useNavigate();
  const [countries, setCountries] = useState<Country[]>([]);
  const [formData, setFormData] = useState<VacationForm>({
    country: "",
    description: "",
    startDate: "",
    endDate: "",
    price: "",
    image: null,
  });

  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [error, setError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if user is admin
    if (!user || user.roleId !== 1) {
      navigate("/");
      return;
    }
    loadCountries();
  }, [user, navigate]);

  const loadCountries = async () => {
    try {
      const countriesData = await api.getCountries();
      setCountries(countriesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load countries");
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { id, value } = e.target;
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFormData((prev) => ({ ...prev, image: file }));
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const countryId = parseInt(formData.country);
      if (!countryId) {
        throw new Error("Please select a country");
      }

      await api.createVacation({
        countryId,
        description: formData.description,
        startDate: formData.startDate,
        endDate: formData.endDate,
        price: parseFloat(formData.price),
        imageName: formData.image?.name,
      });

      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create vacation");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="create-vacation">
      <div className="create-vacation__card">
        <h2 className="create-vacation__title">{TITLE}</h2>

        <form className="create-vacation__form" onSubmit={handleSubmit}>
          {error && <div className="create-vacation__error">{error}</div>}
          {/* Country */}
          <div className="create-vacation__group">
            <label htmlFor="country">{COUNTRY_LABEL}</label>
            <select
              id="country"
              className="create-vacation__input"
              value={formData.country}
              onChange={handleChange}
              required
              disabled={isLoading}
            >
              <option value="">{COUNTRY_PLACEHOLDER}</option>
              {countries.map((country) => (
                <option key={country.id} value={country.id}>
                  {country.name}
                </option>
              ))}
            </select>
          </div>

          {/* Description */}
          <div className="create-vacation__group">
            <label htmlFor="description">{DESCRIPTION_LABEL}</label>
            <textarea
              id="description"
              className="create-vacation__textarea"
              placeholder={DESCRIPTION_PLACEHOLDER}
              value={formData.description}
              onChange={handleChange}
              required
              disabled={isLoading}
            ></textarea>
          </div>

          {/* Dates */}
          <div className="create-vacation__dates">
            <div className="create-vacation__group">
              <label htmlFor="startDate">{START_LABEL}</label>
              <input
                type="date"
                id="startDate"
                className="create-vacation__input"
                value={formData.startDate}
                onChange={handleChange}
                required
                disabled={isLoading}
                min={new Date().toISOString().split('T')[0]}
              />
            </div>

            <div className="create-vacation__group">
              <label htmlFor="endDate">{END_LABEL}</label>
              <input
                type="date"
                id="endDate"
                className="create-vacation__input"
                value={formData.endDate}
                onChange={handleChange}
                required
                disabled={isLoading}
                min={formData.startDate || new Date().toISOString().split('T')[0]}
              />
            </div>
          </div>

          {/* Price */}
          <div className="create-vacation__group">
            <label htmlFor="price">{PRICE_LABEL}</label>
            <div className="create-vacation__price">
              <span>{CURRENCY_SYMBOL}</span>
              <input
                type="number"
                id="price"
                className="create-vacation__input"
                placeholder={PRICE_PLACEHOLDER}
                value={formData.price}
                onChange={handleChange}
                required
                min="0"
                max="10000"
                step="0.01"
                disabled={isLoading}
              />
            </div>
          </div>

          {/* Image */}
          <div className="create-vacation__group">
            <label htmlFor="cover">{COVER_LABEL}</label>
            <div className="create-vacation__image-box">
              {imagePreview ? (
                <img
                  src={imagePreview}
                  alt="preview"
                  className="create-vacation__preview"
                />
              ) : (
                <label htmlFor="cover" className="create-vacation__image-label">
                  {SELECT_IMAGE}
                </label>
              )}
              <input
                type="file"
                id="cover"
                accept="image/*"
                onChange={handleImageChange}
                hidden
              />
            </div>
          </div>

          {/* Buttons */}
          <button type="submit" className="create-vacation__button" disabled={isLoading}>
            {isLoading ? "Creating..." : ADD_BUTTON}
          </button>
          <button
            type="button"
            className="create-vacation__cancel"
            onClick={() => window.history.back()}
          >
            {CANCEL_BUTTON}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateVacation;
