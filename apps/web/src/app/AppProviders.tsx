import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";

import { createBrowserQueryClient } from "./queryClient";

type AppProvidersProps = {
  readonly children: ReactNode;
  readonly queryClient?: QueryClient | undefined;
};

export function AppProviders({ children, queryClient }: AppProvidersProps) {
  const [activeQueryClient] = useState(() => queryClient ?? createBrowserQueryClient());

  return (
    <QueryClientProvider client={activeQueryClient}>{children}</QueryClientProvider>
  );
}
