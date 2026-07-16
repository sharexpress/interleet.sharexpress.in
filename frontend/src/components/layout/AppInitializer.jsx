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

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RouterProvider } from "react-router-dom";

import { router } from "@/routes/AppRoutes";

import { GetCurrentUser } from "@/redux/slices/userSlice";

function AppInitializer() {
  const dispatch = useDispatch();

  const { initialized } = useSelector((state) => state.user);

  useEffect(() => {
    dispatch(GetCurrentUser());
  }, [dispatch]);

  // Block the entire tree until we know the auth state.
  // This prevents route guards from flashing the wrong screen
  // before the cookie-based session is verified.
  if (!initialized) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#0a0a0a]">
        <div className="space-y-4 text-center">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border border-zinc-700 border-t-orange-500" />

          <div>
            <h1 className="text-sm font-medium text-white">Loading Interleet</h1>

            <p className="mt-1 text-xs text-zinc-500">Restoring your session...</p>
          </div>
        </div>
      </div>
    );
  }

  return <RouterProvider router={router} />;
}

export default AppInitializer;
