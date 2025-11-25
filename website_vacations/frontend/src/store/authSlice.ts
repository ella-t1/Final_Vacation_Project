import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { User } from "../utils/api";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Load user from localStorage on initialization
const loadUserFromStorage = (): User | null => {
  try {
    const stored = localStorage.getItem("auth_user");
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (error) {
    console.error("Failed to load user from localStorage:", error);
  }
  return null;
};

const savedUser = loadUserFromStorage();

const initialState: AuthState = {
  user: savedUser,
  isAuthenticated: !!savedUser,
  isLoading: false,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
      state.isAuthenticated = true;
      state.isLoading = false;
      // Save to localStorage
      try {
        localStorage.setItem("auth_user", JSON.stringify(action.payload));
      } catch (error) {
        console.error("Failed to save user to localStorage:", error);
      }
    },
    clearUser: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.isLoading = false;
      // Remove from localStorage
      try {
        localStorage.removeItem("auth_user");
      } catch (error) {
        console.error("Failed to remove user from localStorage:", error);
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
  },
});

export const { setUser, clearUser, setLoading } = authSlice.actions;
export default authSlice.reducer;


