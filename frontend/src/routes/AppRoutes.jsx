import { createBrowserRouter, Navigate } from "react-router-dom";

import { ProtectedRoute, PublicRoute, OnboardingRoute } from "@/routes/RouteGuards";

// Public / marketing
import IndexPage from "@/pages/index";
import LoginPage from "@/pages/login";
import SignupPage from "@/pages/signup";
import ForgotPage from "@/pages/forgot";
import RecruiterPage from "@/pages/recruiter";
import AboutPage from "@/pages/about";
import BlogPage from "@/pages/blog";
import ContactPage from "@/pages/contact";
import ChangelogPage from "@/pages/changelog";
import StatusPage from "@/pages/status";
import SecurityPage from "@/pages/security";
import PrivacyPage from "@/pages/privacy";
import TermsPage from "@/pages/terms";
import CookiesPage from "@/pages/cookies";

// Onboarding
import OnboardingPage from "@/pages/app/Onboarding";

// Protected app pages
import DashboardPage from "@/pages/app/dashboard";
import ChallengesPage from "@/pages/app/challenges/index";
import ChallengePage from "@/pages/app/challenges/$id";
import InterviewsPage from "@/pages/app/interviews/index";
import InterviewReportPage from "@/pages/app/interviews/$id.report";
import InterviewLivePage from "@/pages/app/interviews/live";
import InterviewSetupPage from "@/pages/app/interviews/setup";
import LeaderboardPage from "@/pages/app/leaderboard";
import ProfilePage from "@/pages/app/profile/$username";
import SettingsPage from "@/pages/app/settings";
import SystemDesignPage from "@/pages/app/system-design";
import EditorPage from "@/pages/app/editor.$id";
import StorePage from "@/pages/app/Store";
import ContestList from "@/pages/app/contest/ContestList";
import ContestLobby from "@/pages/app/contest/ContestLobby";
import ContestWorkspace from "@/pages/app/contest/ContestWorkspace";
import ContestResults from "@/pages/app/contest/ContestResults";

import { useSelector } from "react-redux";

// Admin + misc
import AdminPage from "@/pages/admin";
import NotFoundPage from "@/pages/NotFound";

function ProfileRedirect() {
  const { user } = useSelector((state) => state.user);
  if (user && user.username) {
    return <Navigate to={`/app/profile/${user.username}`} replace />;
  }
  return <Navigate to="/app/dashboard" replace />;
}

export const router = createBrowserRouter([
  // ── Fully public (no auth needed, no redirect) ───────────────────────────
  {
    path: "/",
    element: <IndexPage />,
  },
  {
    path: "/about",
    element: <AboutPage />,
  },
  {
    path: "/blog",
    element: <BlogPage />,
  },
  {
    path: "/contact",
    element: <ContactPage />,
  },
  {
    path: "/changelog",
    element: <ChangelogPage />,
  },
  {
    path: "/status",
    element: <StatusPage />,
  },
  {
    path: "/security",
    element: <SecurityPage />,
  },
  {
    path: "/privacy",
    element: <PrivacyPage />,
  },
  {
    path: "/terms",
    element: <TermsPage />,
  },
  {
    path: "/cookies",
    element: <CookiesPage />,
  },
  {
    path: "/recruiter",
    element: <RecruiterPage />,
  },
  {
    path: "/dashboard",
    element: <Navigate to="/app/dashboard" replace />,
  },

  // ── Auth routes (redirect away if already logged in) ─────────────────────
  {
    element: <PublicRoute />,
    children: [
      { path: "/login", element: <LoginPage /> },
      { path: "/signup", element: <LoginPage /> },
      { path: "/forgot", element: <ForgotPage /> },

    ],
  },

  // ── Onboarding (authed but onboarding_completed = false) ─────────────────
  {
    element: <OnboardingRoute />,
    children: [{ path: "/onboarding", element: <OnboardingPage /> }],
  },

  // ── Protected app (authed + onboarding_completed = true) ─────────────────
  {
    element: <ProtectedRoute />,
    children: [
      { path: "/app/dashboard", element: <DashboardPage /> },
      { path: "/app/challenges", element: <ChallengesPage /> },
      { path: "/app/challenges/:id", element: <ChallengePage /> },
      { path: "/app/interviews", element: <InterviewsPage /> },
      { path: "/app/interviews/setup", element: <InterviewSetupPage /> },
      { path: "/app/interviews/:id/report", element: <InterviewReportPage /> },
      { path: "/app/interviews/live", element: <InterviewLivePage /> },
      { path: "/app/leaderboard", element: <LeaderboardPage /> },
      { path: "/app/profile", element: <ProfileRedirect /> },
      { path: "/app/profile/:username", element: <ProfilePage /> },
      { path: "/app/settings", element: <SettingsPage /> },
      { path: "/app/system-design", element: <SystemDesignPage /> },
      { path: "/app/editor/:id", element: <EditorPage /> },
      { path: "/app/contest", element: <ContestList /> },
      { path: "/app/contest/room/:code", element: <ContestLobby /> },
      { path: "/app/contest/editor/:code", element: <ContestWorkspace /> },
      { path: "/app/contest/results/:code", element: <ContestResults /> },
      { path: "/app/store", element: <StorePage /> },

    ],
  },

  // ── Admin ─────────────────────────────────────────────────────────────────
  {
    path: "/admin",
    element: <AdminPage />,
  },

  // ── 404 ───────────────────────────────────────────────────────────────────
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);
