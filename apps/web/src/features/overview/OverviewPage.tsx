import type { PortAtlasApiClient } from "@portatlas/api-client";

import { AssuranceBoundary } from "../../components/AssuranceBoundary";
import { PortInventoryTable } from "../../components/PortInventoryTable";
import { StatusBadge } from "../../components/StatusBadge";
import { syntheticPortRows } from "./foundationData";
import { SystemStatus } from "./SystemStatus";

type OverviewPageProps = {
  readonly apiClient: PortAtlasApiClient;
};

export function OverviewPage({ apiClient }: OverviewPageProps) {
  return (
    <>
      <section aria-labelledby="overview-heading" className="hero-panel">
        <div>
          <p className="eyebrow">Local port intelligence</p>
          <h1 id="overview-heading">Know what is using a port—and why.</h1>
          <p className="hero-copy">
            This engineering foundation keeps runtime observations, declarations,
            reservations, and leases visibly separate. No telemetry leaves this machine.
          </p>
        </div>
        <SystemStatus apiClient={apiClient} />
      </section>

      <section aria-labelledby="capabilities-heading" className="capability-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Foundation capability seams</p>
            <h2 id="capabilities-heading">Core status</h2>
          </div>
          <p className="section-note">Synthetic examples · no machine data</p>
        </div>
        <div className="capability-grid">
          <article>
            <StatusBadge label="Foundation ready" tone="healthy" />
            <h3>Host-neutral domain</h3>
            <p>Core contracts remain testable without Docker or Ollama.</p>
          </article>
          <article>
            <StatusBadge label="Optional" tone="limited" />
            <h3>Docker integration</h3>
            <p>
              A stopped or absent Docker service must not corrupt authoritative state.
            </p>
          </article>
          <article>
            <StatusBadge label="Disabled by default" tone="neutral" />
            <h3>Local AI</h3>
            <p>
              Generated output remains advisory and has no authority over mutations.
            </p>
          </article>
        </div>
      </section>

      <AssuranceBoundary />

      <section aria-labelledby="inventory-heading" className="inventory-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Table integration seam</p>
            <h2 id="inventory-heading">Port evidence preview</h2>
          </div>
          <p className="section-note">Fixture data is always labeled</p>
        </div>
        <PortInventoryTable rows={syntheticPortRows} />
      </section>
    </>
  );
}
