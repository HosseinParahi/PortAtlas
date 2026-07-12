# Gate 3 Native Packaging Research

- **Status:** Bounded feasibility spike complete; no packaging selection or lifecycle acceptance
- **Date:** 2026-07-13
- **Scope:** `G3-20` research only
- **Release owner:** Gate 9

## Question

Can the private Python foundation produce and execute a disposable native macOS CLI bundle without adding packaging tools to the default environment or implying a release artifact?

This spike does not implement installation, a background service, browser bootstrap, signing identity, notarization, update, rollback, or uninstall. It does not select PyInstaller as the release packager.

## Controlled experiment

The repository-local `scripts/packaging_spike.py` used the locked packaging group in an automatically deleted temporary directory. It built a one-directory PyInstaller bundle, ran its `version` and `--help` commands, recorded bounded metadata, and removed the bundle when the process exited.

| Input | Observed value |
| --- | --- |
| Host | macOS 26.5.2, arm64 |
| Python | 3.13.14 |
| PyInstaller | 6.21.0 |
| Private foundation version | `0.0.0.dev0` |
| Bundle size | 24,251,708 bytes |
| Disposable tree SHA-256 | `281329a5456e0acd101705b50fb1e11195a1b17f6e4fe4cac99f53b166c82b4e` |
| CLI version smoke | `PortAtlas (working title) 0.0.0.dev0` |
| CLI help smoke | Passed |
| Developer signing identity used | No |
| Notarization submitted or probed | No |
| Artifact retained or published | No |

After the experiment, the default frozen environment was synchronized again. Its isolation check confirmed that PyInstaller, Docker, MCP, Ollama, psutil, and psycopg were absent.

## Findings

- A private arm64 CLI bundle is technically feasible with the accepted Python baseline.
- The spike exercised only the CLI composition seam. It did not prove that the future service, built React assets, authentication bootstrap, database migration, or background lifecycle can be packaged safely.
- PyInstaller reconciled a macOS SDK-version difference between its executable and the managed Python library. Gate 9 must measure the supported deployment target and verify behavior on clean supported macOS machines rather than accepting that rewrite implicitly.
- The build process performed only tool-generated local executable signing needed for the temporary binary. It did not use a founder identity, Developer ID, notarization, or release signature.
- A 24 MB foundation-only tree is a planning measurement, not a release-size target. Future service and web assets will change it materially.
- The experiment emitted build logs containing machine-local temporary paths. Such raw logs are not release evidence; only the redacted facts above may be retained.

## Gate 9 experiment plan

Before accepting native packaging, Gate 9 must:

1. compare PyInstaller with at least one equivalent native Python bundling approach against the accepted service/web composition;
2. prove user-scoped install, loopback start, one-time browser bootstrap, stop, restart, crash recovery, and no-admin operation;
3. verify Developer ID signing, notarization, artifact hashes, minimum macOS deployment target, Apple-silicon clean-machine behavior, and any separately approved Intel profile;
4. exercise migration failure, backup, rollback, upgrade, credential rotation, diagnostics, and complete uninstall with explicit data retention choices;
5. verify that uninstall never touches registered project sources, Docker resources, Ollama models, or global toolchains; and
6. repeat the working-name and public namespace gate before producing a distributable identity.

## Disposition

`G3-20` has research evidence only. ADR 0007 remains Proposed, no release package exists, and Gate 9 retains packaging implementation and acceptance authority.
