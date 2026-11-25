import { writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { config } from "dotenv";

config({ path: resolve(import.meta.dirname, ".env") });

const API_URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev";
const API_KEY = process.env.NVIDIA_API_KEY;

function usage() {
  console.error("Usage: node generate-image.mjs <prompt> [cfg_scale] [steps] [seed] [output.png]");
  console.error("");
  console.error("Arguments:");
  console.error("  prompt     (required) Text description of the image");
  console.error("  cfg_scale  (optional, default: 5)  Classifier-free guidance scale. Higher = more faithful to prompt (1-20)");
  console.error("  steps      (optional, default: 25) Denoising steps. Higher = more detail but slower (1-50)");
  console.error("  seed       (optional) Random seed for reproducible results (integer)");
  console.error("  output     (optional, default: flux-<timestamp>.png) Output filename");
  process.exit(1);
}

const PROMPT = process.argv[2];

if (!PROMPT) usage();

if (!API_KEY) {
  console.error("Error: NVIDIA_API_KEY not found.");
  console.error("");
  console.error("To use this skill you need an API key from build.nvidia.com:");
  console.error("  1. Go to https://build.nvidia.com/black-forest-labs/flux-1-dev");
  console.error("  2. Sign in and generate an API key");
  console.error("  3. Save it in the .env file as:");
  console.error("     NVIDIA_API_KEY=nvapi-...");
  process.exit(1);
}

const cfgScale = process.argv[3] ? parseFloat(process.argv[3]) : 5;
const steps = process.argv[4] ? parseInt(process.argv[4], 10) : 25;
const seed = process.argv[5] ? parseInt(process.argv[5], 10) : undefined;
const OUTPUT = process.argv[6] || `flux-${Date.now()}.png`;

const body = { prompt: PROMPT, cfg_scale: cfgScale, steps };
if (seed !== undefined) body.seed = seed;

console.error(`Generating with: prompt="${PROMPT.slice(0, 80)}..." cfg_scale=${cfgScale} steps=${steps}${seed !== undefined ? ` seed=${seed}` : ""}`);

const response = await fetch(API_URL, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
  body: JSON.stringify(body),
});

if (!response.ok) {
  const text = await response.text();
  console.error(`API error ${response.status}: ${text}`);
  process.exit(1);
}

const data = await response.json();

let buffer = null;

if (data.artifacts?.[0]?.base64) {
  const b64 = data.artifacts[0].base64;
  buffer = Buffer.from(b64, "base64");
} else if (data.image) {
  const b64 = data.image.replace(/^data:image\/\w+;base64,/, "");
  buffer = Buffer.from(b64, "base64");
} else if (Buffer.isBuffer(data) || data instanceof ArrayBuffer) {
  buffer = Buffer.from(data);
} else {
  const json = JSON.stringify(data).slice(0, 500);
  console.error(`Unknown response format: ${json}`);
  process.exit(1);
}

const outPath = resolve(OUTPUT);
await writeFile(outPath, buffer);
console.log(outPath);
