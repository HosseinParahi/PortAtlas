import type { QueryClient } from "@tanstack/react-query";

import { createApiClient, type PortAtlasApiClient } from "@portatlas/api-client";

import { AppProviders } from "./app/AppProviders";
import { OverviewPage } from "./features/overview/OverviewPage";

type AppProps = {
  readonly apiClient?: PortAtlasApiClient | undefined;
  readonly queryClient?: QueryClient | undefined;
};

const navigationItems = [
  { available: true, label: "Overview" },
  { available: false, label: "Ports" },
  { available: false, label: "Projects" },
  { available: false, label: "Conflicts" },
  { available: false, label: "Reservations" },
  { available: false, label: "Activity" },
  { available: false, label: "Integrations" },
  { available: false, label: "Settings" },
  { available: false, label: "Help" },
] as const;

export function App({ apiClient = createApiClient(), queryClient }: AppProps) {
  return (
    <AppProviders queryClient={queryClient}>
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <div className="working-title-banner" role="note">
        <strong>PortAtlas is a working title.</strong>
        <span>
          No public package, image, domain, or manifest namespace has been released.
        </span>
      </div>
      <header className="app-header">
        <a
          aria-label="PortAtlas working-title overview"
          className="brand"
          href="#overview-heading"
        >
          <span aria-hidden="true" className="brand-mark">
            PA
          </span>
          <span>
            PortAtlas
            <small>Working title</small>
          </span>
        </a>
        <div className="privacy-mark">
          <span aria-hidden="true">⌂</span>
          Local only · no telemetry
        </div>
      </header>
      <div className="demo-banner" role="note">
        <span aria-hidden="true">◇</span>
        <strong>Foundation preview:</strong> all inventory rows on this screen are
        synthetic.
      </div>
      <div className="app-layout">
        <nav aria-label="Primary" className="primary-navigation">
          <p className="navigation-label">Workspace</p>
          <ul>
            {navigationItems.map((item) => (
              <li key={item.label}>
                {item.available ? (
                  <a aria-current="page" href="#overview-heading">
                    <span aria-hidden="true" className="nav-marker">
                      ◆
                    </span>
                    {item.label}
                  </a>
                ) : (
                  <span aria-disabled="true" className="nav-item nav-item--planned">
                    <span aria-hidden="true" className="nav-marker">
                      ◇
                    </span>
                    <span>{item.label}</span>
                    <small>Planned</small>
                  </span>
                )}
              </li>
            ))}
          </ul>
        </nav>
        <main id="main-content" tabIndex={-1}>
          <OverviewPage apiClient={apiClient} />
        </main>
        <aside aria-labelledby="scope-heading" className="scope-aside">
          <p className="eyebrow">Current scope</p>
          <h2 id="scope-heading">Registry-only MVP</h2>
          <ul>
            <li>
              <span aria-hidden="true">✓</span> Reservations and atomic leases
            </li>
            <li>
              <span aria-hidden="true">—</span> No source patching
            </li>
            <li>
              <span aria-hidden="true">—</span> No managed launch
            </li>
            <li>
              <span aria-hidden="true">—</span> No process termination
            </li>
          </ul>
        </aside>
      </div>
      <footer>
        <p>Private engineering foundation · Apache-2.0 · commercial use permitted</p>
        <p>Sponsorship is voluntary and never required for usage permission.</p>
      </footer>
    </AppProviders>
  );
}
