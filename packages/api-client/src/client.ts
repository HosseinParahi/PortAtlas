import {
  HEALTH_PATH,
  type CanonicalError,
  type ErrorEnvelope,
  type HealthResponse,
} from "./generated/openapi";

const MAX_RESPONSE_BYTES = 64 * 1024;
const LOOPBACK_HOSTS = new Set(["127.0.0.1", "[::1]", "localhost"]);
const SAFE_REQUEST_ID = /^[A-Za-z0-9._:-]{1,128}$/;
const SAFE_VERSION = /^[0-9A-Za-z.+-]{1,64}$/;

type RequestOptions = {
  readonly signal?: AbortSignal;
};

export type HealthResult = {
  readonly data: HealthResponse;
  readonly requestId: string | null;
};

export type PortAtlasApiClient = {
  readonly health: (options?: RequestOptions) => Promise<HealthResult>;
};

export type ApiClientOptions = {
  /** An origin such as http://127.0.0.1:8765. Empty means same origin. */
  readonly apiOrigin?: string;
  /** Test and native-shell seam; production callers should use the platform fetch. */
  readonly fetch?: typeof fetch;
};

export class PortAtlasApiError extends Error {
  readonly code: string;
  readonly details: Readonly<Record<string, unknown>>;
  readonly requestId: string | null;
  readonly retryable: boolean;
  readonly status: number;

  constructor(error: CanonicalError, status: number) {
    super(error.message);
    this.name = "PortAtlasApiError";
    this.code = error.code;
    this.details = error.details;
    this.requestId = safeRequestId(error.request_id);
    this.retryable = error.retryable;
    this.status = status;
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function safeRequestId(value: string | null): string | null {
  return value !== null && SAFE_REQUEST_ID.test(value) ? value : null;
}

function requestIdFrom(response: Response): string | null {
  return safeRequestId(response.headers.get("X-Request-ID"));
}

function parseHealthResponse(value: unknown): HealthResponse {
  if (
    !isRecord(value) ||
    value.status !== "ok" ||
    value.service !== "portatlas-core" ||
    typeof value.version !== "string" ||
    !SAFE_VERSION.test(value.version) ||
    value.schema_version !== 1
  ) {
    throw new PortAtlasApiError(
      {
        code: "INTERNAL_ERROR",
        message:
          "PortAtlas returned a response that does not match the client contract.",
        retryable: false,
        request_id: "client-contract",
        details: {},
      },
      502,
    );
  }

  return {
    schema_version: 1,
    service: "portatlas-core",
    status: "ok",
    version: value.version,
  };
}

function parseErrorEnvelope(
  value: unknown,
  fallbackRequestId: string | null,
): ErrorEnvelope {
  if (!isRecord(value) || !isRecord(value.error)) {
    return fallbackError(fallbackRequestId);
  }

  const { error } = value;
  if (
    typeof error.code !== "string" ||
    typeof error.message !== "string" ||
    typeof error.retryable !== "boolean" ||
    typeof error.request_id !== "string" ||
    !isRecord(error.details)
  ) {
    return fallbackError(fallbackRequestId);
  }

  return {
    error: {
      code: error.code,
      details: error.details,
      message: error.message,
      request_id: safeRequestId(error.request_id) ?? fallbackRequestId ?? "unavailable",
      retryable: error.retryable,
    },
  };
}

function fallbackError(requestId: string | null): ErrorEnvelope {
  return {
    error: {
      code: "INTERNAL_ERROR",
      details: {},
      message: "PortAtlas returned an unreadable error response.",
      request_id: requestId ?? "unavailable",
      retryable: false,
    },
  };
}

async function readBoundedJson(response: Response): Promise<unknown> {
  const declaredLength = Number(response.headers.get("Content-Length"));
  if (Number.isFinite(declaredLength) && declaredLength > MAX_RESPONSE_BYTES) {
    return undefined;
  }

  const body = await response.text();
  if (new TextEncoder().encode(body).byteLength > MAX_RESPONSE_BYTES) {
    return undefined;
  }

  try {
    return JSON.parse(body) as unknown;
  } catch {
    return undefined;
  }
}

function endpoint(apiOrigin: string, path: string): string {
  const origin = apiOrigin.trim();
  if (origin === "") {
    return path;
  }

  const url = new URL(path, origin.endsWith("/") ? origin : `${origin}/`);
  if (url.protocol !== "http:" && url.protocol !== "https:") {
    throw new TypeError("The API origin must use HTTP or HTTPS.");
  }
  if (url.username !== "" || url.password !== "") {
    throw new TypeError("The API origin must not contain credentials.");
  }
  if (!LOOPBACK_HOSTS.has(url.hostname)) {
    throw new TypeError("The API origin must be loopback-only.");
  }

  return url.toString();
}

export function createApiClient(options: ApiClientOptions = {}): PortAtlasApiClient {
  const fetchImplementation = options.fetch ?? globalThis.fetch;
  const apiOrigin = options.apiOrigin ?? "";

  return {
    async health(requestOptions = {}) {
      const init: RequestInit = {
        credentials: "same-origin",
        headers: { Accept: "application/json" },
        method: "GET",
      };
      if (requestOptions.signal !== undefined) {
        init.signal = requestOptions.signal;
      }

      const response = await fetchImplementation(
        endpoint(apiOrigin, HEALTH_PATH),
        init,
      );
      const requestId = requestIdFrom(response);
      const body = await readBoundedJson(response);

      if (!response.ok) {
        const envelope = parseErrorEnvelope(body, requestId);
        throw new PortAtlasApiError(envelope.error, response.status);
      }

      return { data: parseHealthResponse(body), requestId };
    },
  };
}
