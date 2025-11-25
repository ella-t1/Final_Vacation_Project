/** API utilities for statistics website backend. */

import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

/** Axios instance configured for statistics API. */
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important: sends cookies for session authentication
  headers: {
    'Content-Type': 'application/json',
  },
})

/** User interface from API. */
export interface User {
  id: number
  firstName: string
  lastName: string
  email: string
  username?: string
  roleId: number
}

/** Login request interface. */
export interface LoginRequest {
  username?: string
  email?: string
  password: string
}

/** Vacation statistics response. */
export interface VacationStats {
  pastVacations: number
  ongoingVacations: number
  futureVacations: number
}

/** Total users response. */
export interface TotalUsers {
  totalUsers: number
}

/** Total likes response. */
export interface TotalLikes {
  totalLikes: number
}

/** Likes distribution item. */
export interface LikesDistributionItem {
  destination: string
  likes: number
}

/** API service class. */
class ApiService {
  /**
   * Login with username/email and password.
   * @param credentials - Login credentials
   * @returns User data if successful
   */
  async login(credentials: LoginRequest): Promise<User> {
    const response = await api.post<User>('/login', credentials)
    return response.data
  }

  /**
   * Logout current user.
   */
  async logout(): Promise<void> {
    await api.post('/logout')
  }

  /**
   * Get vacation statistics (past, ongoing, future).
   * @returns Vacation statistics
   */
  async getVacationStats(): Promise<VacationStats> {
    const response = await api.get<VacationStats>('/vacations/stats')
    return response.data
  }

  /**
   * Get total number of users.
   * @returns Total users count
   */
  async getTotalUsers(): Promise<TotalUsers> {
    const response = await api.get<TotalUsers>('/users/total')
    return response.data
  }

  /**
   * Get total number of likes.
   * @returns Total likes count
   */
  async getTotalLikes(): Promise<TotalLikes> {
    const response = await api.get<TotalLikes>('/likes/total')
    return response.data
  }

  /**
   * Get likes distribution by destination.
   * @returns Array of destination and likes count
   */
  async getLikesDistribution(): Promise<LikesDistributionItem[]> {
    const response = await api.get<LikesDistributionItem[]>('/likes/distribution')
    return response.data
  }
}

export const apiService = new ApiService()

