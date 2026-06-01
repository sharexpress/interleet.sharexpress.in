import { createSlice } from "@reduxjs/toolkit";
import { challenges as mockChallenges } from "@/lib/mock";






const initialState = {
  items: mockChallenges,
  selectedId: null
};

const challengesSlice = createSlice({
  name: "challenges",
  initialState,
  reducers: {
    selectChallenge: (state, action) => {
      state.selectedId = action.payload;
    },
    clearSelection: (state) => {
      state.selectedId = null;
    }
  }
});

export const { selectChallenge, clearSelection } = challengesSlice.actions;
export default challengesSlice.reducer;