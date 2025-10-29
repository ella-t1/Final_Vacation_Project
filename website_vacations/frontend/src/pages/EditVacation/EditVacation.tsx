import { CONSTS } from "../../consts/consts";
import "./EditVacation.scss";
import { useState, useEffect } from "react";

interface VacationData {
  country: string;
  description: string;
  startDate: string;
  endDate: string;
  price: number;
  image: string;
}

const EditVacation = () => {
  const [vacation, setVacation] = useState<VacationData>({
    country: "Rhodes",
    description:
      "It's time to take a break and enjoy a cocktail by the sea on a Rhodes vacation. Incredible seaside views are there for the taking on a...",
    startDate: "2022-11-08",
    endDate: "2022-11-22",
    price: 462,
    image:
      "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=900&q=80",
  });

  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const {TITLE, COUNTRY_LABEL, COUNTRY_PLACEHOLDER, DESCRIPTION_LABEL, START_LABEL, END_LABEL, PRICE_LABEL, CURRENCY_SYMBOL, COVER_LABEL, CHANGE_IMAGE, SELECT_IMAGE, UPDATE_BUTTON, CANCEL_BUTTON, COUNTRY_OPTIONS} = CONSTS.EDIT_VACATIONS;

  useEffect(() => {
    setImagePreview(vacation.image);
  }, [vacation.image]);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) setImagePreview(URL.createObjectURL(file));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Updated vacation:", vacation);
  };

  return (
    <div className="edit-vacation">
      <div className="edit-vacation__card">
        <h2 className="edit-vacation__title">{TITLE}</h2>

        <form className="edit-vacation__form" onSubmit={handleSubmit}>
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
              <option value="">
                {COUNTRY_PLACEHOLDER}
              </option>
              {COUNTRY_OPTIONS.map((country) => (
                <option key={country} value={country}>
                  {country}
                </option>
              ))}
            </select>
          </div>

          <div className="edit-vacation__group">
            <label htmlFor="description">
              {DESCRIPTION_LABEL}
            </label>
            <textarea
              id="description"
              className="edit-vacation__textarea"
              value={vacation.description}
              onChange={(e) =>
                setVacation({ ...vacation, description: e.target.value })
              }
            ></textarea>
          </div>

          <div className="edit-vacation__dates">
            <div className="edit-vacation__group">
              <label htmlFor="start">
                {START_LABEL}
              </label>
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
                  setVacation({ ...vacation, price: Number(e.target.value) })
                }
              />
            </div>
          </div>

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
