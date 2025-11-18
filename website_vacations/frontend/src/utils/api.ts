const API_BASE_URL = "http://localhost:5000/api";

export interface User {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  roleId: number;
  isAdmin?: boolean;
}

export interface Vacation {
  id: number;
  countryId: number;
  description: string;
  startDate: string;
  endDate: string;
  price: number;
  imageName?: string;
}

export interface Country {
  id: number;
  name: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

export interface CreateVacationRequest {
  countryId: number;
  description: string;
  startDate: string;
  endDate: string;
  price: number;
  imageName?: string;
}

export interface UpdateVacationRequest {
  countryId?: number;
  description?: string;
  startDate?: string;
  endDate?: string;
  price?: number;
  imageName?: string;
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: "Unknown error" }));
      throw new Error(error.error || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // User endpoints
  async register(data: RegisterRequest): Promise<User> {
    return this.request<User>("/users/register", {
      method: "POST",
      body: JSON.stringify({
        firstName: data.firstName,
        lastName: data.lastName,
        email: data.email,
        password: data.password,
      }),
    });
  }

  async login(data: LoginRequest): Promise<User> {
    return this.request<User>("/users/login", {
      method: "POST",
      body: JSON.stringify({
        email: data.email,
        password: data.password,
      }),
    });
  }

  async likeVacation(userId: number, vacationId: number): Promise<void> {
    return this.request<void>(`/users/${userId}/likes/${vacationId}`, {
      method: "POST",
    });
  }

  async unlikeVacation(userId: number, vacationId: number): Promise<void> {
    return this.request<void>(`/users/${userId}/likes/${vacationId}`, {
      method: "DELETE",
    });
  }

  async getUserLikes(userId: number): Promise<{ likedVacationIds: number[] }> {
    return this.request<{ likedVacationIds: number[] }>(
      `/users/${userId}/likes`
    );
  }

  // Vacation endpoints
  async getVacations(): Promise<Vacation[]> {
    return this.request<Vacation[]>("/vacations");
  }

  async getVacation(vacationId: number): Promise<Vacation> {
    return this.request<Vacation>(`/vacations/${vacationId}`);
  }

  async createVacation(data: CreateVacationRequest): Promise<Vacation> {
    return this.request<Vacation>("/vacations", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateVacation(
    vacationId: number,
    data: UpdateVacationRequest
  ): Promise<Vacation> {
    return this.request<Vacation>(`/vacations/${vacationId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteVacation(vacationId: number): Promise<void> {
    return this.request<void>(`/vacations/${vacationId}`, {
      method: "DELETE",
    });
  }

  // Country endpoints
  async getCountries(): Promise<Country[]> {
    return this.request<Country[]>("/countries");
  }
}

export const api = new ApiService();

