import { createSlice } from "@reduxjs/toolkit";
import { interviewHistory as mockInterviewHistory } from "@/lib/mock";













const initialState = {
  history: mockInterviewHistory
};

const interviewsSlice = createSlice({
  name: "interviews",
  initialState,
  reducers: {
    addInterview: (state, action) => {
      state.history.unshift(action.payload);
    },
    updateInterviewHistory: (state, action) => {
      state.history = action.payload;
    }
  }
});

export const { addInterview, updateInterviewHistory } = interviewsSlice.actions;
export default interviewsSlice.reducer;