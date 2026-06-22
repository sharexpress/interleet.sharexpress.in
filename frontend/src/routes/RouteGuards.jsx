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

  const isPremiumUser = user?.is_premium || user?.role === "admin";

  // Gate AI Mock Interviews under premium subscription
  if (location.pathname.startsWith("/app/interviews") && !isPremiumUser) {
    return <Navigate to="/app/store" replace />;
  }

  return <Outlet />;
}
