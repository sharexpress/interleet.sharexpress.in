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
