import { createSlice } from "@reduxjs/toolkit";
import { leaderboard as mockLeaderboard } from "@/lib/mock";





const initialState = {
  items: mockLeaderboard
};

const leaderboardSlice = createSlice({
  name: "leaderboard",
  initialState,
  reducers: {
    updateLeaderboard: (state, action) => {
      state.items = action.payload;
    }
  }
});

export const { updateLeaderboard } = leaderboardSlice.actions;
export default leaderboardSlice.reducer;