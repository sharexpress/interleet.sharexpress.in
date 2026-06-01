import { createBrowserRouter } from "react-router-dom";
import NotFound from "@/pages/NotFound";
import Page0 from "@/pages/index";
import Page1 from "@/pages/app/settings";
import Page2 from "@/pages/app/system-design";
import Page3 from "@/pages/app/leaderboard";
import Page4 from "@/pages/app/dashboard";
import Page5 from "@/pages/app/challenges/index";
import Page6, { loader as Page6Loader } from "@/pages/app/challenges/$id";
import Page7, { loader as Page7Loader } from "@/pages/app/editor.$id";
import Page8 from "@/pages/app/profile/$username";
import Page9 from "@/pages/app/interviews/index";
import Page10 from "@/pages/app/interviews/$id.report";
import Page11 from "@/pages/app/interviews/live";
import Page12 from "@/pages/login";
import Page13 from "@/pages/signup";
import Page14 from "@/pages/recruiter";
import Page15 from "@/pages/forgot";
import Page16 from "@/pages/admin";

export const router = createBrowserRouter([
  { path: "/", element: <Page0 /> },
  { path: "/app/settings", element: <Page1 /> },
  { path: "/app/system-design", element: <Page2 /> },
  { path: "/app/leaderboard", element: <Page3 /> },
  { path: "/app/dashboard", element: <Page4 /> },
  { path: "/app/challenges", element: <Page5 /> },
  { path: "/app/challenges/:id", element: <Page6 />, loader: Page6Loader },
  { path: "/app/editor/:id", element: <Page7 />, loader: Page7Loader },
  { path: "/app/profile/:username", element: <Page8 /> },
  { path: "/app/interviews", element: <Page9 /> },
  { path: "/app/interviews/:id/report", element: <Page10 /> },
  { path: "/app/interviews/live", element: <Page11 /> },
  { path: "/login", element: <Page12 /> },
  { path: "/signup", element: <Page13 /> },
  { path: "/recruiter", element: <Page14 /> },
  { path: "/forgot", element: <Page15 /> },
  { path: "/admin", element: <Page16 /> },
  { path: "*", element: <NotFound /> }
]);
