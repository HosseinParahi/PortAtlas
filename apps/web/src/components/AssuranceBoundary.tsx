import { AssuranceDialog } from "./AssuranceDialog";

export function AssuranceBoundary() {
  return (
    <section aria-labelledby="assurance-heading" className="assurance-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Product truth</p>
          <h2 id="assurance-heading">Managed and unmanaged assurance</h2>
        </div>
        <AssuranceDialog />
      </div>
      <div className="assurance-grid">
        <article>
          <p className="assurance-label">
            <span aria-hidden="true">◆</span> Cooperating clients
          </p>
          <h3>Atomic registry coordination</h3>
          <p>
            Reservations and leases are committed atomically for clients that honor the
            PortAtlas registry. That prevents two cooperating clients from receiving the
            same allocation.
          </p>
        </article>
        <article>
          <p className="assurance-label">
            <span aria-hidden="true">△</span> Unmanaged processes
          </p>
          <h3>Evidence, not a conflict-proof guarantee</h3>
          <p>
            Discovery is point-in-time evidence. An external process can ignore the
            registry or bind after a check, so suggestions and observations never claim
            future availability.
          </p>
        </article>
      </div>
    </section>
  );
}
