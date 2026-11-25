import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { config } from "dotenv";

config({ path: resolve(import.meta.dirname, ".env") });

const API_URL = "https://ai.api.nvidia.com/v1/vlm/google/paligemma";
const API_KEY = process.env.NVIDIA_API_KEY;

function usage() {
  console.error("Usage: node describe-image.mjs <image_path> [prompt]");
  console.error("");
  console.error("Arguments:");
  console.error("  image_path  (required) Path to the image file (png, jpg, etc.)");
  console.error("  prompt      (optional, default: 'Describe this image in detail') Text prompt for the description");
  process.exit(1);
}

const IMAGE_PATH = process.argv[2];
const PROMPT = process.argv[3] || "Describe this image in detail";

if (!IMAGE_PATH) usage();

if (!API_KEY) {
  console.error("Error: NVIDIA_API_KEY not found.");
  console.error("");
  console.error("To use this skill you need an API key from build.nvidia.com:");
  console.error("  1. Go to https://build.nvidia.com/black-forest-labs/flux-1-dev"); 
  console.error("     (or https://build.nvidia.com/google/paligemma)");
  console.error("  2. Sign in and generate an API key");
  console.error("  3. Save it in the .env file as:");
  console.error("     NVIDIA_API_KEY=nvapi-...");
  process.exit(1);
}

const imageBuffer = await readFile(resolve(IMAGE_PATH));
const base64Image = imageBuffer.toString("base64");

console.error(`Describing image: ${IMAGE_PATH} with prompt: "${PROMPT}"`);

const response = await fetch(API_URL, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
  body: JSON.stringify({
    messages: [
      {
        role: "user",
        content: [
          { type: "image_url", image_url: `data:image/png;base64,${base64Image}` },
          { type: "text", text: PROMPT },
        ],
      },
    ],
  }),
});

if (!response.ok) {
  const text = await response.text();
  console.error(`API error ${response.status}: ${text}`);
  process.exit(1);
}

const data = await response.json();
const description = data.choices?.[0]?.message?.content || JSON.stringify(data, null, 2);
console.log(description);
