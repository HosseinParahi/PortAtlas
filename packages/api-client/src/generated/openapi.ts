// Generated from contracts/openapi/v1.json. Do not edit by hand.

export type ApiSchemas = {
  readonly "CanonicalError": { readonly "code": string; readonly "details": { readonly [key: string]: unknown; }; readonly "message": string; readonly "request_id": string; readonly "retryable": boolean; };
  readonly "ErrorEnvelope": { readonly "error": ApiSchemas["CanonicalError"]; };
  readonly "HealthResponse": { readonly "schema_version": 1; readonly "service": "portatlas-core"; readonly "status": "ok"; readonly "version": string; };
  readonly "ReadinessReport": { readonly "components": { readonly [key: string]: "ready" | "degraded" | "unavailable"; }; readonly "schema_version": 1; readonly "status": "ready" | "degraded"; };
};

export const HEALTH_PATH = "/api/v1/health" as const;

export type HealthResponse = ApiSchemas["HealthResponse"];
export type CanonicalError = ApiSchemas["CanonicalError"];
export type ErrorEnvelope = ApiSchemas["ErrorEnvelope"];

export type HealthOperation = {
  readonly method: "GET";
  readonly path: typeof HEALTH_PATH;
  readonly response: HealthResponse;
};
