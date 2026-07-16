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