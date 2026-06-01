import { createSlice } from "@reduxjs/toolkit";
import { activityWeekly as mockActivityWeekly, recentActivity as mockRecentActivity } from "@/lib/mock";



















const initialState = {
  weekly: mockActivityWeekly,
  recent: mockRecentActivity
};

const activitySlice = createSlice({
  name: "activity",
  initialState,
  reducers: {
    updateWeeklyActivity: (state, action) => {
      state.weekly = action.payload;
    },
    updateRecentActivity: (state, action) => {
      state.recent = action.payload;
    },
    addRecentActivity: (state, action) => {
      state.recent.unshift(action.payload);
    }
  }
});

export const { updateWeeklyActivity, updateRecentActivity, addRecentActivity } = activitySlice.actions;
export default activitySlice.reducer;