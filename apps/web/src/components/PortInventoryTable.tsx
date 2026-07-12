import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useMemo } from "react";

import { StatusBadge, type StatusTone } from "./StatusBadge";

export type PortInventoryRow = {
  readonly assurance: "Cooperating registry" | "Runtime evidence";
  readonly port: number;
  readonly project: string;
  readonly protocol: "TCP" | "UDP";
  readonly source: string;
  readonly state: "Observed" | "Reserved";
  readonly tone: StatusTone;
};

const columnHelper = createColumnHelper<PortInventoryRow>();

const columns = [
  columnHelper.accessor("port", {
    cell: (context) => <strong>{context.getValue()}</strong>,
    header: "Port",
  }),
  columnHelper.accessor("protocol", { header: "Protocol" }),
  columnHelper.accessor("state", {
    cell: (context) => (
      <StatusBadge label={context.getValue()} tone={context.row.original.tone} />
    ),
    header: "State",
  }),
  columnHelper.accessor("project", { header: "Project instance" }),
  columnHelper.accessor("source", { header: "Evidence source" }),
  columnHelper.accessor("assurance", { header: "Assurance" }),
];

type PortInventoryTableProps = {
  readonly rows: readonly PortInventoryRow[];
};

export function PortInventoryTable({ rows }: PortInventoryTableProps) {
  const tableRows = useMemo(() => [...rows], [rows]);
  // TanStack Table intentionally exposes closures that React Compiler does not memoize.
  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    columns,
    data: tableRows,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div
      aria-label="Scrollable port evidence table"
      className="table-scroll"
      role="region"
      // A focusable named region lets keyboard users scroll a wide semantic table.
      // eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex
      tabIndex={0}
    >
      <table>
        <caption>
          Synthetic Gate 3 fixture showing separate runtime evidence and cooperative
          registry state
        </caption>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id} scope="col">
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
