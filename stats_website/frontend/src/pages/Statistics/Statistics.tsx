import { useEffect, useState } from 'react'
import { apiService } from '../../utils/api'
import type {
  VacationStats,
  TotalUsers,
  TotalLikes,
  LikesDistributionItem,
} from '../../utils/api'
import Nav from '../../components/Nav/Nav'
import './Statistics.scss'

const Statistics = () => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [vacationStats, setVacationStats] = useState<VacationStats | null>(null)
  const [totalUsers, setTotalUsers] = useState<TotalUsers | null>(null)
  const [totalLikes, setTotalLikes] = useState<TotalLikes | null>(null)
  const [likesDistribution, setLikesDistribution] = useState<LikesDistributionItem[]>([])

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        setLoading(true)
        setError(null)

        const [vacStats, users, likes, distribution] = await Promise.all([
          apiService.getVacationStats(),
          apiService.getTotalUsers(),
          apiService.getTotalLikes(),
          apiService.getLikesDistribution(),
        ])

        setVacationStats(vacStats)
        setTotalUsers(users)
        setTotalLikes(likes)
        setLikesDistribution(distribution)
      } catch (err: any) {
        setError(err.response?.data?.error || err.message || 'Failed to load statistics')
      } finally {
        setLoading(false)
      }
    }

    fetchStatistics()
  }, [])

  if (loading) {
    return (
      <div className="statistics">
        <Nav />
        <div className="statistics-container">
          <div className="loading">Loading statistics...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="statistics">
        <Nav />
        <div className="statistics-container">
          <div className="error-message">
            <span>⚠️</span> {error}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="statistics">
      <Nav />
      <div className="statistics-container">
        <h1 className="statistics-title">System Statistics</h1>

        {/* Vacation Statistics */}
        <section className="statistics-section">
          <h2 className="section-title">Vacation Statistics</h2>
          <div className="stats-grid">
            <div className="stat-card stat-card-past">
              <div className="stat-icon">📅</div>
              <div className="stat-value">{vacationStats?.pastVacations || 0}</div>
              <div className="stat-label">Past Vacations</div>
            </div>
            <div className="stat-card stat-card-ongoing">
              <div className="stat-icon">✈️</div>
              <div className="stat-value">{vacationStats?.ongoingVacations || 0}</div>
              <div className="stat-label">Ongoing Vacations</div>
            </div>
            <div className="stat-card stat-card-future">
              <div className="stat-icon">🗓️</div>
              <div className="stat-value">{vacationStats?.futureVacations || 0}</div>
              <div className="stat-label">Future Vacations</div>
            </div>
          </div>
        </section>

        {/* User and Likes Statistics */}
        <section className="statistics-section">
          <h2 className="section-title">User & Engagement Statistics</h2>
          <div className="stats-grid">
            <div className="stat-card stat-card-users">
              <div className="stat-icon">👥</div>
              <div className="stat-value">{totalUsers?.totalUsers || 0}</div>
              <div className="stat-label">Total Users</div>
            </div>
            <div className="stat-card stat-card-likes">
              <div className="stat-icon">❤️</div>
              <div className="stat-value">{totalLikes?.totalLikes || 0}</div>
              <div className="stat-label">Total Likes</div>
            </div>
          </div>
        </section>

        {/* Likes Distribution */}
        <section className="statistics-section">
          <h2 className="section-title">Likes Distribution by Destination</h2>
          {likesDistribution.length === 0 ? (
            <div className="no-data">No likes data available</div>
          ) : (
            <div className="distribution-table">
              <table>
                <thead>
                  <tr>
                    <th>Destination</th>
                    <th>Likes</th>
                  </tr>
                </thead>
                <tbody>
                  {likesDistribution.map((item, index) => (
                    <tr key={index}>
                      <td>{item.destination}</td>
                      <td className="likes-count">{item.likes}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  )
}

export default Statistics

