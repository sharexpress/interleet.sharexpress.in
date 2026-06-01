import { createSlice } from "@reduxjs/toolkit";
import { user as mockUser } from "@/lib/mock";






















const initialState = mockUser;

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    updateUser: (state, action) => {
      return { ...state, ...action.payload };
    },
    incrementXP: (state, action) => {
      state.xp += action.payload;
    },
    updateStreak: (state, action) => {
      state.streak = action.payload;
    }
  }
});

export const { updateUser, incrementXP, updateStreak } = userSlice.actions;
export default userSlice.reducer;