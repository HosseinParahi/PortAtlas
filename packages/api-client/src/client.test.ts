import { describe, expect, it } from "vitest";

import { PortAtlasApiError, createApiClient } from "./client";

function jsonResponse(body: unknown, init: ResponseInit = {}): Response {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  return new Response(JSON.stringify(body), { ...init, headers });
}

describe("PortAtlas API client", () => {
  it("reads the generated health contract without exposing transport details", async () => {
    let requestedUrl = "";
    let requestedInit: RequestInit | undefined;
    const fetchImplementation: typeof fetch = (input, init) => {
      requestedUrl =
        typeof input === "string"
          ? input
          : input instanceof URL
            ? input.href
            : input.url;
      requestedInit = init;
      return Promise.resolve(
        jsonResponse(
          {
            schema_version: 1,
            service: "portatlas-core",
            status: "ok",
            version: "0.0.0.dev0",
          },
          { headers: { "X-Request-ID": "req_test-1" } },
        ),
      );
    };

    const client = createApiClient({
      apiOrigin: "http://127.0.0.1:8765",
      fetch: fetchImplementation,
    });

    await expect(client.health()).resolves.toEqual({
      data: {
        schema_version: 1,
        service: "portatlas-core",
        status: "ok",
        version: "0.0.0.dev0",
      },
      requestId: "req_test-1",
    });
    expect(requestedUrl).toBe("http://127.0.0.1:8765/api/v1/health");
    expect(requestedInit).toMatchObject({
      credentials: "same-origin",
      method: "GET",
    });
  });

  it("maps a safe canonical error without returning arbitrary response fields", async () => {
    const fetchImplementation: typeof fetch = () =>
      Promise.resolve(
        jsonResponse(
          {
            error: {
              code: "AUTHENTICATION_REQUIRED",
              details: { safe_hint: "bootstrap" },
              message: "A local session is required.",
              request_id: "req_auth-1",
              retryable: false,
            },
            ignored: "not copied",
          },
          { status: 401 },
        ),
      );

    const error = await createApiClient({ fetch: fetchImplementation })
      .health()
      .catch((reason: unknown) => reason);

    expect(error).toBeInstanceOf(PortAtlasApiError);
    expect(error).toMatchObject({
      code: "AUTHENTICATION_REQUIRED",
      details: { safe_hint: "bootstrap" },
      message: "A local session is required.",
      requestId: "req_auth-1",
      retryable: false,
      status: 401,
    });
  });

  it("rejects a success response that drifts from the generated schema", async () => {
    const fetchImplementation: typeof fetch = () =>
      Promise.resolve(jsonResponse({ service: "different-service", status: "ok" }));

    const error = await createApiClient({ fetch: fetchImplementation })
      .health()
      .catch((reason: unknown) => reason);

    expect(error).toBeInstanceOf(PortAtlasApiError);
    expect(error).toMatchObject({ code: "INTERNAL_ERROR", status: 502 });
  });

  it("rejects a non-loopback API origin before making a request", async () => {
    let called = false;
    const fetchImplementation: typeof fetch = () => {
      called = true;
      return Promise.resolve(jsonResponse({}));
    };

    const client = createApiClient({
      apiOrigin: "https://example.invalid",
      fetch: fetchImplementation,
    });

    await expect(client.health()).rejects.toThrow("loopback-only");
    expect(called).toBe(false);
  });
});
