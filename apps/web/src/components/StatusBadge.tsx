export type StatusTone = "healthy" | "limited" | "neutral" | "warning";

type StatusBadgeProps = {
  readonly label: string;
  readonly tone: StatusTone;
};

const stateIcons: Readonly<Record<StatusTone, string>> = {
  healthy: "✓",
  limited: "!",
  neutral: "•",
  warning: "△",
};

export function StatusBadge({ label, tone }: StatusBadgeProps) {
  return (
    <span className="status-badge" data-state={tone}>
      <span aria-hidden="true" className="status-badge__icon">
        {stateIcons[tone]}
      </span>
      <span>{label}</span>
    </span>
  );
}
