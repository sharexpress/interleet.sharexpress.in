import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";

import { store } from "@/redux";

import AppInitializer from "@/components/layout/AppInitializer";

import { Toaster } from "@/components/ui/sonner";

import "@/styles.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Provider store={store}>
      <AppInitializer />

      <Toaster />
    </Provider>
  </StrictMode>,
);
