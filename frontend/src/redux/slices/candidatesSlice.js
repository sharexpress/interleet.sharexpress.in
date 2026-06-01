import { createSlice } from "@reduxjs/toolkit";
import { candidates as mockCandidates } from "@/lib/mock";














const initialState = {
  items: mockCandidates
};

const candidatesSlice = createSlice({
  name: "candidates",
  initialState,
  reducers: {
    updateCandidates: (state, action) => {
      state.items = action.payload;
    }
  }
});

export const { updateCandidates } = candidatesSlice.actions;
export default candidatesSlice.reducer;