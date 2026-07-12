import type { PortInventoryRow } from "../../components/PortInventoryTable";

export const syntheticPortRows: readonly PortInventoryRow[] = [
  {
    assurance: "Runtime evidence",
    port: 3000,
    project: "demo-web / main checkout",
    protocol: "TCP",
    source: "Synthetic host observation",
    state: "Observed",
    tone: "healthy",
  },
  {
    assurance: "Cooperating registry",
    port: 4310,
    project: "demo-api / feature worktree",
    protocol: "TCP",
    source: "Synthetic reservation",
    state: "Reserved",
    tone: "neutral",
  },
];
