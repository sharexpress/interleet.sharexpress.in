import { configureStore } from "@reduxjs/toolkit";
import challengesReducer from "./slices/challengesSlice";
import userReducer from "./slices/userSlice";
import leaderboardReducer from "./slices/leaderboardSlice";
import activityReducer from "./slices/activitySlice";
import interviewsReducer from "./slices/interviewsSlice";
import systemDesignReducer from "./slices/systemDesignSlice";
import candidatesReducer from "./slices/candidatesSlice";
import simulatorReducer from "./slices/simulatorSlice";
import challengeExecutionReducer from "./slices/challengeExecutionSlice";

export const store = configureStore({
  reducer: {
    challenges: challengesReducer,
    user: userReducer,
    leaderboard: leaderboardReducer,
    activity: activityReducer,
    interviews: interviewsReducer,
    systemDesign: systemDesignReducer,
    candidates: candidatesReducer,
    simulator: simulatorReducer,
    challengeExecution: challengeExecutionReducer,
  },
});