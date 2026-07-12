import * as axe from "axe-core";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { QueryClient } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import type { PortAtlasApiClient } from "@portatlas/api-client";

import { App } from "./App";

const stylesheetPath = [
  resolve(process.cwd(), "src/styles/index.css"),
  resolve(process.cwd(), "apps/web/src/styles/index.css"),
].find(existsSync);
if (stylesheetPath === undefined) {
  throw new Error("browser foundation stylesheet is unavailable to its contract test");
}
const styles = readFileSync(stylesheetPath, "utf8");

const healthyClient: PortAtlasApiClient = {
  health: () =>
    Promise.resolve({
      data: {
        schema_version: 1,
        service: "portatlas-core",
        status: "ok",
        version: "0.0.0.dev0",
      },
      requestId: "req_ui-test",
    }),
};

function renderApp(apiClient: PortAtlasApiClient = healthyClient) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return render(<App apiClient={apiClient} queryClient={queryClient} />);
}

describe("browser foundation", () => {
  it("labels the working title, demo boundary, privacy posture, and semantic landmarks", async () => {
    renderApp();

    expect(screen.getByText("PortAtlas is a working title.")).toBeVisible();
    expect(
      screen.getByText(/all inventory rows on this screen are synthetic/i),
    ).toBeVisible();
    expect(screen.getByRole("navigation", { name: "Primary" })).toBeVisible();
    expect(
      screen.getByText("Ports").closest("[aria-disabled='true']"),
    ).toHaveTextContent("Planned");
    expect(screen.getByRole("main")).toBeVisible();
    expect(
      screen.getByRole("complementary", { name: "Registry-only MVP" }),
    ).toBeVisible();
    expect(screen.getByRole("contentinfo")).toHaveTextContent(
      "commercial use permitted",
    );
    expect(await screen.findByText("Local core available")).toBeVisible();
    expect(screen.getByText(/Local only · no telemetry/i)).toBeVisible();
  });

  it("states managed and unmanaged assurance without relying on color", () => {
    renderApp();

    expect(
      screen.getByRole("heading", { name: "Atomic registry coordination" }),
    ).toBeVisible();
    expect(
      screen.getByRole("heading", { name: "Evidence, not a conflict-proof guarantee" }),
    ).toBeVisible();
    expect(
      screen.getByText(/An external process can ignore the registry/i),
    ).toBeVisible();
    expect(screen.getByText("Observed")).toBeVisible();
    expect(screen.getByText("Reserved")).toBeVisible();
  });

  it("keeps the synthetic shell intact when the authoritative core is unavailable", async () => {
    const unavailableClient: PortAtlasApiClient = {
      health: () => Promise.reject(new Error("synthetic unavailable core")),
    };

    renderApp(unavailableClient);

    expect(await screen.findByText("Local core unavailable")).toBeVisible();
    expect(
      screen.getByText(/authoritative local data is not available/i),
    ).toBeVisible();
    expect(screen.getByText("Synthetic host observation")).toBeVisible();
  });

  it("locks compact-layout and reduced-motion accessibility contracts", () => {
    expect(styles).toContain("@media (max-width: 54rem)");
    expect(styles).toContain("@media (max-width: 38rem)");
    expect(styles).toContain("@media (prefers-reduced-motion: reduce)");
    expect(styles).toContain("animation-duration: 0.01ms !important");
    expect(styles).toContain("scroll-behavior: auto !important");
  });

  it("uses an accessible table for separate evidence and registry fixture rows", () => {
    renderApp();

    const table = screen.getByRole("table", {
      name: /Synthetic Gate 3 fixture showing separate runtime evidence/i,
    });
    expect(table).toBeVisible();
    expect(screen.getAllByRole("columnheader")).toHaveLength(6);
    expect(screen.getByText("Synthetic host observation")).toBeVisible();
    expect(screen.getByText("Synthetic reservation")).toBeVisible();
  });

  it("returns focus to the Radix dialog trigger after Escape", async () => {
    const user = userEvent.setup();
    renderApp();
    const trigger = screen.getByRole("button", { name: "Review assurance details" });

    await user.click(trigger);
    expect(
      screen.getByRole("dialog", { name: "What PortAtlas can assure" }),
    ).toBeVisible();
    expect(screen.getByRole("button", { name: "Close details" })).toHaveFocus();

    await user.keyboard("{Escape}");
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(trigger).toHaveFocus();
  });

  it("has no automatically detectable accessibility violations in the shell", async () => {
    const { container } = renderApp();
    await screen.findByText("Local core available");

    const results = await axe.run(container, {
      rules: {
        "color-contrast": { enabled: false },
      },
    });

    expect(results.violations).toEqual([]);
  });
});
