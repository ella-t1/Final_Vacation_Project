import { useEffect, useState } from "react";
import "./Homepage.scss";
import { api, Vacation, Country } from "../../utils/api";
import { useAppSelector } from "../../hooks/useAppSelector";
import { useNavigate } from "react-router-dom";

const Homepage = () => {
  const [vacations, setVacations] = useState<Vacation[]>([]);
  const [countries, setCountries] = useState<Country[]>([]);
  const [likedVacations, setLikedVacations] = useState<Set<number>>(new Set());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const user = useAppSelector((state) => state.auth.user);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, [user]);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [vacationsData, countriesData] = await Promise.all([
        api.getVacations(),
        api.getCountries(),
      ]);
      // Sort vacations by start date ascending
      const sortedVacations = [...vacationsData].sort((a, b) => {
        const dateA = new Date(a.startDate).getTime();
        const dateB = new Date(b.startDate).getTime();
        return dateA - dateB;
      });
      setVacations(sortedVacations);
      setCountries(countriesData);

      // Load user likes if logged in
      if (user) {
        try {
          const likes = await api.getUserLikes(user.id);
          setLikedVacations(new Set(likes.likedVacationIds));
        } catch (err) {
          console.error("Failed to load likes:", err);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load vacations");
    } finally {
      setIsLoading(false);
    }
  };

  const getCountryName = (countryId: number): string => {
    const country = countries.find((c) => c.id === countryId);
    return country?.name || "Unknown";
  };

  const handleLike = async (vacationId: number) => {
    if (!user) {
      navigate("/login");
      return;
    }

    try {
      const isLiked = likedVacations.has(vacationId);
      if (isLiked) {
        await api.unlikeVacation(user.id, vacationId);
        setLikedVacations((prev) => {
          const newSet = new Set(prev);
          newSet.delete(vacationId);
          return newSet;
        });
      } else {
        await api.likeVacation(user.id, vacationId);
        setLikedVacations((prev) => new Set(prev).add(vacationId));
      }
      // Reload vacations to update likes count
      const vacationsData = await api.getVacations();
      const sortedVacations = [...vacationsData].sort((a, b) => {
        const dateA = new Date(a.startDate).getTime();
        const dateB = new Date(b.startDate).getTime();
        return dateA - dateB;
      });
      setVacations(sortedVacations);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to update like");
    }
  };

  const handleDelete = async (vacationId: number) => {
    if (!user || user.roleId !== 1) {
      return;
    }

    if (!confirm("Are you sure you want to delete this vacation?")) {
      return;
    }

    try {
      await api.deleteVacation(vacationId);
      setVacations((prev) => prev.filter((v) => v.id !== vacationId));
      setLikedVacations((prev) => {
        const newSet = new Set(prev);
        newSet.delete(vacationId);
        return newSet;
      });
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to delete vacation");
    }
  };

  if (isLoading) {
    return (
      <div className="homepage">
        <div className="homepage__loading">Loading vacations...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="homepage">
        <div className="homepage__error">{error}</div>
      </div>
    );
  }

  return (
    <div className="homepage">
      <div className="homepage__container">
        <h1 className="homepage__title">Vacations</h1>
        {user && user.roleId === 1 && (
          <button
            className="homepage__add-button"
            onClick={() => navigate("/create-vacation")}
          >
            Add New Vacation
          </button>
        )}
        <div className="homepage__vacations">
          {vacations.length === 0 ? (
            <div className="homepage__empty">No vacations available</div>
          ) : (
            vacations.map((vacation) => (
              <div key={vacation.id} className="homepage__vacation-card">
                {vacation.imageName && (
                  <div className="homepage__image-container">
                    <img
                      src={`http://localhost:5000/images/${vacation.imageName}`}
                      alt={vacation.description}
                      className="homepage__image"
                      onError={(e) => {
                        (e.target as HTMLImageElement).style.display = "none";
                      }}
                    />
                  </div>
                )}
                <div className="homepage__content">
                  <h2 className="homepage__country">
                    {getCountryName(vacation.countryId)}
                  </h2>
                  <p className="homepage__description">{vacation.description}</p>
                  <div className="homepage__details">
                    <span className="homepage__date">
                      {new Date(vacation.startDate).toLocaleDateString()} -{" "}
                      {new Date(vacation.endDate).toLocaleDateString()}
                    </span>
                    <span className="homepage__price">${vacation.price}</span>
                  </div>
                  <div className="homepage__likes-info">
                    <span className="homepage__likes-count">
                      ❤️ Like {vacation.likesCount || 0}
                    </span>
                  </div>
                  <div className="homepage__actions">
                    {user && user.roleId !== 1 && (
                      <button
                        className={`homepage__like-button ${
                          likedVacations.has(vacation.id) ? "liked" : ""
                        }`}
                        onClick={() => handleLike(vacation.id)}
                      >
                        {likedVacations.has(vacation.id) ? "❤️ Liked" : "🤍 Like"}
                      </button>
                    )}
                    {user && user.roleId === 1 && (
                      <>
                        <button
                          className="homepage__edit-button"
                          onClick={() => navigate(`/edit-vacation/${vacation.id}`)}
                        >
                          Edit
                        </button>
                        <button
                          className="homepage__delete-button"
                          onClick={() => handleDelete(vacation.id)}
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Homepage;
