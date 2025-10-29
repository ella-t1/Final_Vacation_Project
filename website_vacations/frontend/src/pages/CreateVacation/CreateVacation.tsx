import { CONSTS } from "../../consts/consts";
import "./CreateVacation.scss";
import { useState } from "react";

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
    COUNTRY_OPTIONS,
  } = CONSTS.CREATE_VACATIONS;

  const [formData, setFormData] = useState<VacationForm>({
    country: "",
    description: "",
    startDate: "",
    endDate: "",
    price: "",
    image: null,
  });

  const [imagePreview, setImagePreview] = useState<string | null>(null);

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Vacation submitted:", formData);
  };

  return (
    <div className="create-vacation">
      <div className="create-vacation__card">
        <h2 className="create-vacation__title">{TITLE}</h2>

        <form className="create-vacation__form" onSubmit={handleSubmit}>
          {/* Country */}
          <div className="create-vacation__group">
            <label htmlFor="country">{COUNTRY_LABEL}</label>
            <select
              id="country"
              className="create-vacation__input"
              value={formData.country}
              onChange={handleChange}
            >
              <option value="">{COUNTRY_PLACEHOLDER}</option>
              {COUNTRY_OPTIONS.map((country) => (
                <option key={country} value={country}>
                  {country}
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
          <button type="submit" className="create-vacation__button">
            {ADD_BUTTON}
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
