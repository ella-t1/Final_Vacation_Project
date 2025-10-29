import { CONSTS } from "../../consts/consts";
import { useState, useEffect } from "react";
import "./EditVacation.scss"
interface VacationData {
  country: string;
  description: string;
  startDate: string;
  endDate: string;
  price: string;
  image: File | null;
}

const EditVacation = () => {
  const [vacation, setVacation] = useState<VacationData>({
    country: "",
    description: "",
    startDate: "",
    endDate: "",
    price: "",
    image: null,
  });

  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const {
    TITLE,
    COUNTRY_LABEL,
    COUNTRY_PLACEHOLDER,
    DESCRIPTION_LABEL,
    START_LABEL,
    END_LABEL,
    PRICE_LABEL,
    CURRENCY_SYMBOL,
    COVER_LABEL,
    CHANGE_IMAGE,
    SELECT_IMAGE,
    UPDATE_BUTTON,
    CANCEL_BUTTON,
    COUNTRY_OPTIONS,
  } = CONSTS.EDIT_VACATIONS;

  // ✅ Convert File to preview URL if exists
  useEffect(() => {
    if (vacation.image) {
      const objectUrl = URL.createObjectURL(vacation.image);
      setImagePreview(objectUrl);
      return () => URL.revokeObjectURL(objectUrl); // cleanup
    } else {
      setImagePreview(null);
    }
  }, [vacation.image]);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setVacation((prev) => ({ ...prev, image: file }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Updated vacation:", vacation);
    // TODO: send update to backend
  };

  return (
    <div className="edit-vacation">
      <div className="edit-vacation__card">
        <h2 className="edit-vacation__title">{TITLE}</h2>

        <form className="edit-vacation__form" onSubmit={handleSubmit}>
          {/* Country */}
          <div className="edit-vacation__group">
            <label htmlFor="country">{COUNTRY_LABEL}</label>
            <select
              id="country"
              className="edit-vacation__input"
              value={vacation.country}
              onChange={(e) =>
                setVacation({ ...vacation, country: e.target.value })
              }
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
          <div className="edit-vacation__group">
            <label htmlFor="description">{DESCRIPTION_LABEL}</label>
            <textarea
              id="description"
              className="edit-vacation__textarea"
              value={vacation.description}
              onChange={(e) =>
                setVacation({ ...vacation, description: e.target.value })
              }
            ></textarea>
          </div>

          {/* Dates */}
          <div className="edit-vacation__dates">
            <div className="edit-vacation__group">
              <label htmlFor="start">{START_LABEL}</label>
              <input
                type="date"
                id="start"
                className="edit-vacation__input"
                value={vacation.startDate}
                onChange={(e) =>
                  setVacation({ ...vacation, startDate: e.target.value })
                }
              />
            </div>

            <div className="edit-vacation__group">
              <label htmlFor="end">{END_LABEL}</label>
              <input
                type="date"
                id="end"
                className="edit-vacation__input"
                value={vacation.endDate}
                onChange={(e) =>
                  setVacation({ ...vacation, endDate: e.target.value })
                }
              />
            </div>
          </div>

          {/* Price */}
          <div className="edit-vacation__group">
            <label htmlFor="price">{PRICE_LABEL}</label>
            <div className="edit-vacation__price">
              <span>{CURRENCY_SYMBOL}</span>
              <input
                type="number"
                id="price"
                className="edit-vacation__input"
                value={vacation.price}
                onChange={(e) =>
                  setVacation({ ...vacation, price: e.target.value })
                }
              />
            </div>
          </div>

          {/* Image */}
          <div className="edit-vacation__group">
            <label htmlFor="cover">{COVER_LABEL}</label>
            <div className="edit-vacation__image-box">
              {imagePreview ? (
                <label
                  htmlFor="cover"
                  className="edit-vacation__image-label overlay"
                >
                  {CHANGE_IMAGE}
                  <img
                    src={imagePreview}
                    alt="Vacation preview"
                    className="edit-vacation__preview"
                  />
                </label>
              ) : (
                <label htmlFor="cover" className="edit-vacation__image-label">
                  {SELECT_IMAGE}
                </label>
              )}
              <input
                type="file"
                id="cover"
                accept="image/*"
                hidden
                onChange={handleImageChange}
              />
            </div>
          </div>

          {/* Buttons */}
          <button type="submit" className="edit-vacation__button">
            {UPDATE_BUTTON}
          </button>
          <button
            type="button"
            className="edit-vacation__cancel"
            onClick={() => window.history.back()}
          >
            {CANCEL_BUTTON}
          </button>
        </form>
      </div>
    </div>
  );
};

export default EditVacation;
