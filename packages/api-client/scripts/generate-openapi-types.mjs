import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const packageDirectory = resolve(scriptDirectory, "..");
const schemaPath = resolve(packageDirectory, "../../contracts/openapi/v1.json");
const outputPath = resolve(packageDirectory, "src/generated/openapi.ts");
const checkOnly = process.argv.includes("--check");

function invariant(condition, message) {
  if (!condition) {
    throw new Error(`OpenAPI foundation contract invalid: ${message}`);
  }
}

function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function referenceName(reference) {
  const prefix = "#/components/schemas/";
  invariant(reference.startsWith(prefix), `unsupported reference ${reference}`);
  return reference.slice(prefix.length);
}

function schemaType(schema) {
  invariant(isRecord(schema), "schema must be an object");

  if (Object.keys(schema).length === 0) {
    return "unknown";
  }

  if (typeof schema.$ref === "string") {
    return `ApiSchemas[${JSON.stringify(referenceName(schema.$ref))}]`;
  }

  if (Array.isArray(schema.anyOf)) {
    invariant(schema.anyOf.length > 0, "anyOf must not be empty");
    return schema.anyOf.map((member) => schemaType(member)).join(" | ");
  }

  if ("const" in schema) {
    return JSON.stringify(schema.const);
  }

  if (Array.isArray(schema.enum)) {
    invariant(schema.enum.length > 0, "enum must not be empty");
    return schema.enum.map((value) => JSON.stringify(value)).join(" | ");
  }

  switch (schema.type) {
    case "string":
      return "string";
    case "integer":
    case "number":
      return "number";
    case "boolean":
      return "boolean";
    case "array":
      return `ReadonlyArray<${schemaType(schema.items)}>`;
    case "object": {
      const properties = isRecord(schema.properties) ? schema.properties : {};
      const required = new Set(Array.isArray(schema.required) ? schema.required : []);
      const members = Object.entries(properties).map(([name, property]) => {
        const optional = required.has(name) ? "" : "?";
        return `readonly ${JSON.stringify(name)}${optional}: ${schemaType(property)};`;
      });

      if (schema.additionalProperties === true) {
        members.push("readonly [key: string]: unknown;");
      } else if (isRecord(schema.additionalProperties)) {
        members.push(
          `readonly [key: string]: ${schemaType(schema.additionalProperties)};`,
        );
      }

      return `{ ${members.join(" ")} }`;
    }
    default:
      throw new Error(
        `OpenAPI foundation contract invalid: unsupported schema type ${String(schema.type)}`,
      );
  }
}

const specification = JSON.parse(await readFile(schemaPath, "utf8"));
invariant(isRecord(specification), "root must be an object");
invariant(specification.openapi === "3.1.0", "OpenAPI revision must be 3.1.0");

const paths = specification.paths;
invariant(isRecord(paths), "paths must be an object");
const healthPath = "/api/v1/health";
const healthPathItem = paths[healthPath];
invariant(isRecord(healthPathItem), `${healthPath} must exist`);
const healthOperation = healthPathItem.get;
invariant(isRecord(healthOperation), `${healthPath} must define GET`);
invariant(
  healthOperation.operationId === "getHealth",
  "health operationId must be getHealth",
);

const responses = healthOperation.responses;
invariant(isRecord(responses), "health responses must be an object");
const successResponse = responses["200"];
invariant(isRecord(successResponse), "health must define a 200 response");
const responseContent = successResponse.content;
invariant(isRecord(responseContent), "health 200 response must define content");
const jsonResponse = responseContent["application/json"];
invariant(isRecord(jsonResponse), "health 200 response must be JSON");
const successSchema = jsonResponse.schema;
invariant(isRecord(successSchema), "health 200 response must define a schema");
invariant(
  successSchema.$ref === "#/components/schemas/HealthResponse",
  "health 200 response must use HealthResponse",
);

const components = specification.components;
invariant(isRecord(components), "components must be an object");
const schemas = components.schemas;
invariant(isRecord(schemas), "components.schemas must be an object");

for (const requiredSchema of ["HealthResponse", "CanonicalError", "ErrorEnvelope"]) {
  invariant(isRecord(schemas[requiredSchema]), `${requiredSchema} must exist`);
}

const generated = `// Generated from contracts/openapi/v1.json. Do not edit by hand.\n\nexport type ApiSchemas = {\n${Object.entries(
  schemas,
)
  .map(([name, schema]) => `  readonly ${JSON.stringify(name)}: ${schemaType(schema)};`)
  .join(
    "\n",
  )}\n};\n\nexport const HEALTH_PATH = ${JSON.stringify(healthPath)} as const;\n\nexport type HealthResponse = ApiSchemas["HealthResponse"];\nexport type CanonicalError = ApiSchemas["CanonicalError"];\nexport type ErrorEnvelope = ApiSchemas["ErrorEnvelope"];\n\nexport type HealthOperation = {\n  readonly method: "GET";\n  readonly path: typeof HEALTH_PATH;\n  readonly response: HealthResponse;\n};\n`;

if (checkOnly) {
  const current = await readFile(outputPath, "utf8").catch(() => "");
  invariant(
    current === generated,
    "generated client types are stale; run pnpm generate",
  );
  process.stdout.write("OpenAPI generated types are current.\n");
} else {
  await writeFile(outputPath, generated, "utf8");
  process.stdout.write("Generated src/generated/openapi.ts.\n");
}
