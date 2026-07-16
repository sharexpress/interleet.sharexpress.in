/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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