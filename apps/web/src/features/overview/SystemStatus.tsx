import { useQuery } from "@tanstack/react-query";

import type { PortAtlasApiClient } from "@portatlas/api-client";

import { StatusBadge } from "../../components/StatusBadge";

type SystemStatusProps = {
  readonly apiClient: PortAtlasApiClient;
};

export function SystemStatus({ apiClient }: SystemStatusProps) {
  const health = useQuery({
    queryFn: ({ signal }) => apiClient.health({ signal }),
    queryKey: ["system", "health"],
  });

  if (health.isPending) {
    return (
      <div aria-live="polite" className="system-status" role="status">
        <StatusBadge label="Checking local core" tone="neutral" />
        <span>
          The inventory remains unavailable until the local health check completes.
        </span>
      </div>
    );
  }

  if (health.isError) {
    return (
      <div aria-live="polite" className="system-status" role="status">
        <StatusBadge label="Local core unavailable" tone="warning" />
        <span>
          Browser presentation is intact; authoritative local data is not available.
        </span>
      </div>
    );
  }

  return (
    <div aria-live="polite" className="system-status" role="status">
      <StatusBadge label="Local core available" tone="healthy" />
      <span>
        Contract v{health.data.data.schema_version} · request{" "}
        {health.data.requestId ?? "not supplied"}
      </span>
    </div>
  );
}
