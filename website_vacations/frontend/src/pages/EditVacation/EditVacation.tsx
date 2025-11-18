import { CONSTS } from "../../consts/consts";
import { useState, useEffect } from "react";
import "./EditVacation.scss";
import { useParams, useNavigate } from "react-router-dom";
import { api, Vacation, Country } from "../../utils/api";
import { useAppSelector } from "../../hooks/useAppSelector";

interface VacationData {
  country: string;
  description: string;
  startDate: string;
  endDate: string;
  price: string;
  image: File | null;
}

const EditVacation = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.auth.user);
  const [countries, setCountries] = useState<Country[]>([]);
  const [vacation, setVacation] = useState<VacationData>({
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
  const [isLoadingData, setIsLoadingData] = useState(true);

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
  } = CONSTS.EDIT_VACATIONS;

  useEffect(() => {
    // Check if user is admin
    if (!user || user.roleId !== 1) {
      navigate("/");
      return;
    }
    loadData();
  }, [user, navigate, id]);

  const loadData = async () => {
    if (!id) {
      navigate("/");
      return;
    }

    try {
      setIsLoadingData(true);
      const [vacationToEdit, countriesData] = await Promise.all([
        api.getVacation(parseInt(id)),
        api.getCountries(),
      ]);

      setCountries(countriesData);
      setVacation({
        country: vacationToEdit.countryId.toString(),
        description: vacationToEdit.description,
        startDate: vacationToEdit.startDate,
        endDate: vacationToEdit.endDate,
        price: vacationToEdit.price.toString(),
        image: null,
      });

      if (vacationToEdit.imageName) {
        setImagePreview(`http://localhost:5000/images/${vacationToEdit.imageName}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load vacation");
    } finally {
      setIsLoadingData(false);
    }
  };

  // ✅ Convert File to preview URL if exists
  useEffect(() => {
    if (vacation.image) {
      const objectUrl = URL.createObjectURL(vacation.image);
      setImagePreview(objectUrl);
      return () => URL.revokeObjectURL(objectUrl); // cleanup
    }
  }, [vacation.image]);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setVacation((prev) => ({ ...prev, image: file }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;

    setError("");
    setIsLoading(true);

    try {
      const countryId = parseInt(vacation.country);
      if (!countryId) {
        throw new Error("Please select a country");
      }

      await api.updateVacation(parseInt(id), {
        countryId,
        description: vacation.description,
        startDate: vacation.startDate,
        endDate: vacation.endDate,
        price: parseFloat(vacation.price),
        imageFile: vacation.image || undefined,
      });

      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update vacation");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingData) {
    return (
      <div className="edit-vacation">
        <div className="edit-vacation__loading">Loading vacation...</div>
      </div>
    );
  }

  return (
    <div className="edit-vacation">
      <div className="edit-vacation__card">
        <h2 className="edit-vacation__title">{TITLE}</h2>

        <form className="edit-vacation__form" onSubmit={handleSubmit}>
          {error && <div className="edit-vacation__error">{error}</div>}
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
          <div className="edit-vacation__group">
            <label htmlFor="description">{DESCRIPTION_LABEL}</label>
            <textarea
              id="description"
              className="edit-vacation__textarea"
              value={vacation.description}
              onChange={(e) =>
                setVacation({ ...vacation, description: e.target.value })
              }
              required
              disabled={isLoading}
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
                required
                disabled={isLoading}
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
                required
                disabled={isLoading}
                min={vacation.startDate}
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
                required
                min="0"
                max="10000"
                step="0.01"
                disabled={isLoading}
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
          <button type="submit" className="edit-vacation__button" disabled={isLoading}>
            {isLoading ? "Updating..." : UPDATE_BUTTON}
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
