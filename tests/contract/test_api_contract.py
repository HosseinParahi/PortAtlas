"""CT-API-001: versioned health, readiness, request ID, and safe error contract."""

from __future__ import annotations

import re
import unittest

from fastapi.testclient import TestClient
from portatlas.api.app import ReadinessReport, create_app


class ApiFoundationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(
            create_app(
                readiness_probe=lambda: ReadinessReport.ready(
                    {"database": "ready", "configuration": "ready"}
                ),
                bearer_token_verifier=lambda candidate: candidate == "test-readiness-credential",
            )
        )

    def test_health_is_minimal_unauthenticated_and_versioned(self) -> None:
        response = self.client.get("/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "portatlas-core",
                "version": "0.0.0.dev0",
                "schema_version": 1,
            },
        )
        self.assertRegex(response.headers["x-request-id"], r"^req_[0-9a-f-]{36}$")

    def test_authenticated_readiness_does_not_expose_paths_or_credentials(self) -> None:
        unauthorized = self.client.get("/api/v1/ready")
        self.assertEqual(unauthorized.status_code, 401)
        self.assertEqual(unauthorized.json()["error"]["code"], "AUTHENTICATION_REQUIRED")

        response = self.client.get(
            "/api/v1/ready",
            headers={"Authorization": "Bearer test-readiness-credential"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ready")
        serialized = response.text.lower()
        self.assertNotIn("token", serialized)
        self.assertNotIn("/users/", serialized)

    def test_degraded_readiness_matches_its_documented_503_schema(self) -> None:
        client = TestClient(
            create_app(
                readiness_probe=lambda: ReadinessReport(
                    status="degraded",
                    components={"database": "unavailable"},
                    schema_version=1,
                ),
                bearer_token_verifier=lambda _candidate: True,
            )
        )

        response = client.get(
            "/api/v1/ready",
            headers={"Authorization": "Bearer synthetic-credential"},
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["status"], "degraded")

        document = client.get("/api/v1/openapi.json").json()
        schema = document["paths"]["/api/v1/ready"]["get"]["responses"]["503"]["content"][
            "application/json"
        ]["schema"]
        references = {item["$ref"] for item in schema["anyOf"]}
        self.assertEqual(
            references,
            {
                "#/components/schemas/ErrorEnvelope",
                "#/components/schemas/ReadinessReport",
            },
        )

    def test_unexpected_readiness_failure_never_echoes_exception_secrets(self) -> None:
        secret = "gh" + "p_" + "A" * 30

        def failing_probe() -> ReadinessReport:
            raise RuntimeError(f"provider failed with {secret}")

        client = TestClient(
            create_app(
                readiness_probe=failing_probe,
                bearer_token_verifier=lambda _candidate: True,
            )
        )

        response = client.get(
            "/api/v1/ready",
            headers={"Authorization": "Bearer synthetic-credential"},
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["error"]["code"], "PERSISTENCE_UNAVAILABLE")
        self.assertNotIn(secret, response.text)

    def test_caller_request_id_is_accepted_only_in_the_safe_shape(self) -> None:
        safe_id = "req_00000000-0000-4000-8000-000000000001"
        accepted = self.client.get("/api/v1/health", headers={"X-Request-ID": safe_id})
        rejected = self.client.get("/api/v1/health", headers={"X-Request-ID": "not-a-request-id"})

        self.assertEqual(accepted.headers["x-request-id"], safe_id)
        self.assertTrue(re.fullmatch(r"req_[0-9a-f-]{36}", rejected.headers["x-request-id"]))

    def test_openapi_exposes_the_canonical_nested_error_contract(self) -> None:
        document = self.client.get("/api/v1/openapi.json").json()
        schemas = document["components"]["schemas"]

        self.assertIn("CanonicalError", schemas)
        self.assertIn("ErrorEnvelope", schemas)
        self.assertEqual(
            set(schemas["HealthResponse"]["required"]),
            {"schema_version", "service", "status", "version"},
        )
        self.assertEqual(
            set(schemas["CanonicalError"]["required"]),
            {"code", "message", "retryable", "request_id", "details"},
        )
        self.assertEqual(
            set(schemas["ReadinessReport"]["required"]),
            {"components", "schema_version", "status"},
        )
        ready_responses = document["paths"]["/api/v1/ready"]["get"]["responses"]
        self.assertIn("401", ready_responses)
        self.assertIn("503", ready_responses)


if __name__ == "__main__":
    unittest.main()
