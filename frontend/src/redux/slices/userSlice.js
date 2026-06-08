import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { API } from "@/api/api";

const initialState = {
  loading: false,
  error: null,
  success: false,

  user: null,

  email: "",
  transactionID: null,

  authStep: "email",

  isAuthenticated: false,
  onboardingCompleted: false,
  initialized: false,
};

export const SendOTP = createAsyncThunk("AUTH/SEND_OTP", async (email, { rejectWithValue }) => {
  try {
    const response = await API.post("/auth/send-otp", { email });
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response?.data || { message: "SEND OTP FAILED" });
  }
});

export const VerifyOTP = createAsyncThunk(
  "AUTH/VERIFY_OTP",
  async ({ transactionID, otp }, { dispatch, rejectWithValue }) => {
    try {
      const response = await API.post("/auth/verify-otp", {
        transactionID,
        OTP: otp,
      });

      // GetCurrentUser runs here and owns isAuthenticated + user + onboardingCompleted
      await dispatch(GetCurrentUser());

      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "VERIFY OTP FAILED" });
    }
  },
);

export const GetCurrentUser = createAsyncThunk(
  "AUTH/GET_CURRENT_USER",
  async (_, { rejectWithValue }) => {
    try {
      const response = await API.get("/auth/me");
      return response.data;
    } catch (error) {
      return rejectWithValue(
        error.response?.data || {
          message: "GET USER FAILED",
          status: error.response?.status,
        },
      );
    }
  },
);

export const googleLogin = createAsyncThunk("AUTH/GOOGLE_LOGIN", async () => {
  window.location.href = `${import.meta.env.VITE_BACKEND_URL || "https://interleet-backend.sharexpress.in"
    }/auth/google/login`;
});

export const githubLogin = createAsyncThunk("AUTH/GITHUB_LOGIN", async () => {
  window.location.href = `${import.meta.env.VITE_BACKEND_URL || "https://interleet-backend.sharexpress.in"
    }/auth/github/login`;
});

export const LogoutUser = createAsyncThunk("AUTH/LOGOUT", async (_, { rejectWithValue }) => {
  try {
    const response = await API.post("/auth/logout");
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response?.data || { message: "LOGOUT FAILED" });
  }
});

export const CompleteOnboarding = createAsyncThunk(
  "AUTH/COMPLETE_ONBOARDING",
  async (payload, { rejectWithValue }) => {
    try {
      const response = await API.post("/auth/complete-onboarding", payload);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "ONBOARDING FAILED" });
    }
  },
);

export const RegisterFace = createAsyncThunk(
  "AUTH/REGISTER_FACE",
  async ({ email, frames, angles, deviceFingerprint }, { dispatch, rejectWithValue }) => {
    try {
      const response = await API.post("/api/face/register", {
        email,
        frames,
        angles,
        device_fingerprint: deviceFingerprint,
      });
      await dispatch(GetCurrentUser());
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "FACE REGISTRATION FAILED" });
    }
  }
);

export const LoginFace = createAsyncThunk(
  "AUTH/LOGIN_FACE",
  async ({ email, frame, deviceFingerprint }, { dispatch, rejectWithValue }) => {
    try {
      const response = await API.post("/api/face/login", {
        email,
        frame,
        device_fingerprint: deviceFingerprint,
      });
      await dispatch(GetCurrentUser());
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "FACE LOGIN FAILED" });
    }
  }
);

const userSlice = createSlice({
  name: "user",

  initialState,

  reducers: {
    setEmail(state, action) {
      state.email = action.payload;
    },

    clearError(state) {
      state.error = null;
    },

    resetAuthFlow(state) {
      state.authStep = "email";
      state.transactionID = null;
      state.error = null;
      state.success = false;
    },
  },

  extraReducers: (builder) => {
    // ─── SendOTP ────────────────────────────────────────────────────────────
    builder.addCase(SendOTP.pending, (state) => {
      state.loading = true;
      state.error = null;
      state.success = false;
    });

    builder.addCase(SendOTP.fulfilled, (state, action) => {
      state.loading = false;
      state.error = null;
      state.success = true;
      state.authStep = "otp";
      state.transactionID = action.payload?.transactionID || null;
    });

    builder.addCase(SendOTP.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload?.detail || action.payload?.message || "SEND OTP FAILED";
      state.success = false;
    });

    // ─── VerifyOTP ──────────────────────────────────────────────────────────
    // GetCurrentUser is awaited inside the thunk, so by the time
    // VerifyOTP.fulfilled fires, GetCurrentUser has already resolved and
    // set user / isAuthenticated / onboardingCompleted correctly.
    // We only manage loading + error + success here — nothing else.
    builder.addCase(VerifyOTP.pending, (state) => {
      state.loading = true;
      state.error = null;
      state.success = false;
    });

    builder.addCase(VerifyOTP.fulfilled, (state) => {
      state.loading = false;
      state.error = null;
      state.success = true;
      // isAuthenticated, user, onboardingCompleted are owned by GetCurrentUser
    });

    builder.addCase(VerifyOTP.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload?.detail || action.payload?.message || "VERIFY OTP FAILED";
      state.success = false;
      state.isAuthenticated = false;
    });

    // ─── GetCurrentUser ─────────────────────────────────────────────────────
    // Backend now returns lowercase { success, user } — see auth router fix.
    builder.addCase(GetCurrentUser.pending, (state) => {
      state.loading = true;
    });

    builder.addCase(GetCurrentUser.fulfilled, (state, action) => {
      state.loading = false;
      state.initialized = true;
      state.user = action.payload.user;
      state.isAuthenticated = true;
      state.onboardingCompleted = action.payload.user?.onboarding_completed || false;
    });

    builder.addCase(GetCurrentUser.rejected, (state) => {
      state.loading = false;
      state.initialized = true;
      state.user = null;
      state.isAuthenticated = false;
      state.onboardingCompleted = false;
    });

    // ─── LogoutUser ─────────────────────────────────────────────────────────
    builder.addCase(LogoutUser.pending, (state) => {
      state.loading = true;
    });

    builder.addCase(LogoutUser.fulfilled, (state) => {
      state.loading = false;
      state.user = null;
      state.isAuthenticated = false;
      state.authStep = "email";
      state.email = "";
      state.transactionID = null;
      state.error = null;
      state.success = false;
    });

    builder.addCase(LogoutUser.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload?.detail || action.payload?.message || "LOGOUT FAILED";
    });

    // ─── CompleteOnboarding ─────────────────────────────────────────────────
    // Backend returns lowercase { success, message, user }
    builder.addCase(CompleteOnboarding.pending, (state) => {
      state.loading = true;
      state.error = null;
    });

    builder.addCase(CompleteOnboarding.fulfilled, (state, action) => {
      state.loading = false;
      state.user = action.payload?.user;
      state.onboardingCompleted = true;
      state.isAuthenticated = true;
      state.success = true;
    });

    builder.addCase(CompleteOnboarding.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload?.detail || action.payload?.message || "ONBOARDING FAILED";
    });

    // ─── RegisterFace ───────────────────────────────────────────────────────
    builder.addCase(RegisterFace.pending, (state) => {
      state.loading = true;
      state.error = null;
      state.success = false;
    });

    builder.addCase(RegisterFace.fulfilled, (state) => {
      state.loading = false;
      state.success = true;
      state.error = null;
    });

    builder.addCase(RegisterFace.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload?.detail || action.payload?.message || "FACE REGISTRATION FAILED";
      state.success = false;
    });

    // ─── LoginFace ──────────────────────────────────────────────────────────
    builder.addCase(LoginFace.pending, (state) => {
      state.loading = true;
      state.error = null;
      state.success = false;
    });

    builder.addCase(LoginFace.fulfilled, (state) => {
      state.loading = false;
      state.success = true;
      state.error = null;
    });

    builder.addCase(LoginFace.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload?.detail || action.payload?.message || "FACE LOGIN FAILED";
      state.success = false;
    });
  },
});

export const { setEmail, clearError, resetAuthFlow } = userSlice.actions;

export default userSlice.reducer;
