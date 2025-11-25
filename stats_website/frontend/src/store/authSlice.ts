import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { apiService, LoginRequest, User } from '../utils/api'

export interface AuthState {
  isAuthenticated: boolean
  user: User | null
  loading: boolean
  error: string | null
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null,
}

/** Async thunk for login. */
export const loginAsync = createAsyncThunk(
  'auth/login',
  async (credentials: LoginRequest, { rejectWithValue }) => {
    try {
      const user = await apiService.login(credentials)
      return user
    } catch (error: any) {
      const message = error.response?.data?.error || error.message || 'Login failed'
      return rejectWithValue(message)
    }
  }
)

/** Async thunk for logout. */
export const logoutAsync = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      await apiService.logout()
    } catch (error: any) {
      const message = error.response?.data?.error || error.message || 'Logout failed'
      return rejectWithValue(message)
    }
  }
)

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginAsync.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(loginAsync.fulfilled, (state, action) => {
        state.loading = false
        state.isAuthenticated = true
        state.user = action.payload
        state.error = null
      })
      .addCase(loginAsync.rejected, (state, action) => {
        state.loading = false
        state.isAuthenticated = false
        state.user = null
        state.error = action.payload as string
      })

    // Logout
    builder
      .addCase(logoutAsync.pending, (state) => {
        state.loading = true
      })
      .addCase(logoutAsync.fulfilled, (state) => {
        state.loading = false
        state.isAuthenticated = false
        state.user = null
        state.error = null
      })
      .addCase(logoutAsync.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
        // Still logout even if API call fails
        state.isAuthenticated = false
        state.user = null
      })
  },
})

export const { clearError } = authSlice.actions
export default authSlice.reducer
