import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { RouterProvider } from "react-router-dom";

import { store } from "@/redux";
import { router } from "@/routes/AppRoutes";

import { Toaster } from "@/components/ui/sonner";

import "@/styles.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Provider store={store}>
      <RouterProvider
        router={router}
        future={{
          v7_startTransition: true,
        }}
      />

      <Toaster />
    </Provider>
  </StrictMode>,
);
