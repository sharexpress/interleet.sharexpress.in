import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
const API = "http://localhost:8000";

export const sendOTP = createAsyncThunk("user/sendOTP", async (email, thunkAPI) => {
  try {
    const response = await axios.post(`${API}/auth/send-otp`, { email });
    return response.data;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || { message: "Failed to send OTP" });
  }
});

export const verifyOTP = createAsyncThunk("user/verifyOTP", async (payload, thunkAPI) => {
  try {
    const response = await axios.post(
      `${API}/auth/verify-otp`,
      { transactionID: payload.transactionID, OTP: payload.otp },
      { withCredentials: true },
    );
    return response.data;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || { message: "OTP verification failed" });
  }
});

export const googleLogin = createAsyncThunk("user/googleLogin", async (_, thunkAPI) => {
  try {
    window.location.href = `${API}/auth/google/login`;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || { message: "Google login failed" });
  }
});

export const githubLogin = createAsyncThunk("user/githubLogin", async (_, thunkAPI) => {
  try {
    window.location.href = `${API}/auth/github/login`;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || { message: "GitHub login failed" });
  }
});

export const getCurrentUser = createAsyncThunk("user/getCurrentUser", async (_, thunkAPI) => {
  try {
    const response = await axios.get(`${API}/auth/me`, { withCredentials: true });
    return response.data;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || { message: "Failed to fetch user" });
  }
});

export const completeOnboarding = createAsyncThunk(
  "user/completeOnboarding",
  async (payload, thunkAPI) => {
    try {
      const response = await axios.patch(`${API}/user/onboarding`, payload, {
        withCredentials: true,
      });
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data || { message: "Failed to complete onboarding" },
      );
    }
  },
);

export const logoutUser = createAsyncThunk("user/logoutUser", async (_, thunkAPI) => {
  try {
    const response = await axios.post(`${API}/auth/logout`, {}, { withCredentials: true });
    return response.data;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || { message: "Logout failed" });
  }
});

const normalizeError = (payload) => {
  const detail = payload?.detail;
  if (!detail) return payload?.message ?? "Something went wrong";
  if (Array.isArray(detail)) return detail.map((e) => e.msg).join(", ");
  return detail;
};

const initialState = {
  loading: false,
  error: null,
  isAuthenticated: false,
  authStep: "email",
  email: "",
  otp: "",
  transactionID: "",
  user: null,
  onboardingCompleted: false,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setEmail: (state, action) => {
      state.email = action.payload;
    },
    setOTP: (state, action) => {
      state.otp = action.payload;
    },
    setAuthStep: (state, action) => {
      state.authStep = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    resetAuthFlow: (state) => {
      state.authStep = "email";
      state.email = "";
      state.otp = "";
      state.transactionID = "";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendOTP.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendOTP.fulfilled, (state, action) => {
        state.loading = false;
        state.transactionID = action.payload.transactionID;
        state.authStep = "otp";
      })
      .addCase(sendOTP.rejected, (state, action) => {
        state.loading = false;
        state.error = normalizeError(action.payload);
      })

      .addCase(verifyOTP.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(verifyOTP.fulfilled, (state) => {
        state.loading = false;

        state.isAuthenticated = true;
      })
      .addCase(verifyOTP.rejected, (state, action) => {
        state.loading = false;
        state.error = normalizeError(action.payload);
      })

      .addCase(getCurrentUser.pending, (state) => {
        state.loading = true;
      })
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.onboardingCompleted = action.payload.user?.onboarding_completed || false;
      })
      .addCase(getCurrentUser.rejected, (state) => {
        state.loading = false;
        state.isAuthenticated = false;
        state.user = null;
      })

      .addCase(completeOnboarding.pending, (state) => {
        state.loading = true;
      })
      .addCase(completeOnboarding.fulfilled, (state, action) => {
        state.loading = false;
        state.onboardingCompleted = true;
        state.user = action.payload.user;
      })
      .addCase(completeOnboarding.rejected, (state, action) => {
        state.loading = false;
        state.error = normalizeError(action.payload);
      })

      .addCase(logoutUser.fulfilled, () => {
        return initialState;
      });
  },
});

export const { setEmail, setOTP, setAuthStep, clearError, resetAuthFlow } = userSlice.actions;

export default userSlice.reducer;
