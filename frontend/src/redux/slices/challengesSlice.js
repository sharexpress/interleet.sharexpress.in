import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { API } from "@/api/api";

// ── Thunks ────────────────────────────────────────────────────────────────────

export const FetchChallenges = createAsyncThunk(
  "CHALLENGES/FETCH_LIST",
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await API.get("/challenges", { params });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "Failed to fetch challenges" });
    }
  },
);

export const FetchChallengeBySlug = createAsyncThunk(
  "CHALLENGES/FETCH_BY_SLUG",
  async (slug, { getState, rejectWithValue }) => {
    // Return cached detail if we already have it
    const cached = getState().challenges.detail[slug];
    if (cached) return { slug, data: cached };

    try {
      const response = await API.get(`/challenges/${slug}`);
      return { slug, data: response.data.data };
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "Challenge not found" });
    }
  },
);

// ── Initial state ─────────────────────────────────────────────────────────────

const initialState = {
  // List view
  items: [],
  domains: [],
  total: 0,
  loading: false,
  error: null,

  // Detail / editor — keyed by slug for cache
  detail: {}, // { [slug]: challengeObject }
  detailLoading: false,
  detailError: null,
};

// ── Slice ─────────────────────────────────────────────────────────────────────

const challengesSlice = createSlice({
  name: "challenges",
  initialState,
  reducers: {
    clearDetailError(state) {
      state.detailError = null;
    },
  },
  extraReducers: (builder) => {
    // ── FetchChallenges ──────────────────────────────────────────────────────
    builder
      .addCase(FetchChallenges.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(FetchChallenges.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.data ?? [];
        state.domains = action.payload.domains ?? [];
        state.total = action.payload.total ?? state.items.length;
      })
      .addCase(FetchChallenges.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.message ?? "Something went wrong";
      });

    // ── FetchChallengeBySlug ─────────────────────────────────────────────────
    builder
      .addCase(FetchChallengeBySlug.pending, (state) => {
        state.detailLoading = true;
        state.detailError = null;
      })
      .addCase(FetchChallengeBySlug.fulfilled, (state, action) => {
        state.detailLoading = false;
        state.detail[action.payload.slug] = action.payload.data;
      })
      .addCase(FetchChallengeBySlug.rejected, (state, action) => {
        state.detailLoading = false;
        state.detailError = action.payload?.message ?? "Challenge not found";
      });
  },
});

// ── Selectors ─────────────────────────────────────────────────────────────────

export const selectChallengesList = (state) => state.challenges.items;
export const selectChallengesDomains = (state) => state.challenges.domains;
export const selectChallengesTotal = (state) => state.challenges.total;
export const selectChallengesLoading = (state) => state.challenges.loading;
export const selectChallengesError = (state) => state.challenges.error;

export const selectChallengeDetail = (slug) => (state) => state.challenges.detail[slug] ?? null;
export const selectDetailLoading = (state) => state.challenges.detailLoading;
export const selectDetailError = (state) => state.challenges.detailError;

export const { clearDetailError } = challengesSlice.actions;
export default challengesSlice.reducer;
