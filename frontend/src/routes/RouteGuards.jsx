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

import { useSelector } from "react-redux";
import { Navigate, Outlet, useLocation } from "react-router-dom";

/**
 * PublicRoute
 * Redirects already-authenticated users away from auth screens (/login, /signup, /forgot).
 * - authed + onboarding done  → /app/dashboard
 * - authed + onboarding todo  → /onboarding
 * - not authed                → renders the page normally
 */
export function PublicRoute() {
  const { isAuthenticated, onboardingCompleted, initialized } = useSelector((state) => state.user);

  if (!initialized) return null;

  if (isAuthenticated) {
    return onboardingCompleted ? (
      <Navigate to="/app/dashboard" replace />
    ) : (
      <Navigate to="/onboarding" replace />
    );
  }

  return <Outlet />;
}

/**
 * OnboardingRoute
 * Only accessible when authed AND onboarding_completed = false.
 * - not authed                → /login
 * - authed + already done     → /app/dashboard
 */
export function OnboardingRoute() {
  const { isAuthenticated, onboardingCompleted, initialized } = useSelector((state) => state.user);

  if (!initialized) return null;

  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (onboardingCompleted) return <Navigate to="/app/dashboard" replace />;

  return <Outlet />;
}

/**
 * ProtectedRoute
 * Requires authed + onboarding complete.
 * - not authed                → /login
 * - authed + onboarding todo  → /onboarding
 * - authed + not premium      → /app/store (unless already on /app/store)
 */
export function ProtectedRoute() {
  const { isAuthenticated, onboardingCompleted, initialized, user } = useSelector((state) => state.user || {});
  const location = useLocation();

  if (!initialized) return null;

  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (!onboardingCompleted) return <Navigate to="/onboarding" replace />;

  return <Outlet />;
}
