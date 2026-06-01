import { createSlice } from "@reduxjs/toolkit";
import { systemDesignTopics as mockSystemDesignTopics } from "@/lib/mock";

const initialState = {
  topics: mockSystemDesignTopics,
};

const systemDesignSlice = createSlice({
  name: "systemDesign",
  initialState,
  reducers: {
    updateTopics: (state, action) => {
      state.topics = action.payload;
    },
  },
});

export const { updateTopics } = systemDesignSlice.actions;
export default systemDesignSlice.reducer;
