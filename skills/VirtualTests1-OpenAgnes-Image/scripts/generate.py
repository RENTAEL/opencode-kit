import os
import sys
import time
import requests

DEFAULT_MODEL = "agnes-image-2.1-flash"
API_ENDPOINT = "https://apihub.agnes-ai.com/v1/images/generations"
MAX_RETRIES = 3


SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_api_key():
    key = os.environ.get("AGNES_API_KEY")
    if key:
        return key
    env_path = os.path.join(SKILL_ROOT, ".env")
    if os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("AGNES_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip("\"'")
                    if key:
                        return key
    msg = "Error: AGNES_API_KEY not found. Set env var or place .env in: " + SKILL_ROOT
    print(msg, file=sys.stderr)
    print(msg)
    sys.exit(1)


def generate_image(prompt, size="1K", ratio=None, model="agnes-image-2.1-flash", output_path=None):
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "extra_body": {
            "response_format": "url"
        }
    }
    if ratio:
        payload["ratio"] = ratio
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                "https://apihub.agnes-ai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=180,
            )
            if resp.status_code == 503 and attempt < MAX_RETRIES - 1:
                time.sleep(3)
                continue
            if resp.status_code != 200:
                err = f"Error: API returned {resp.status_code}\n{resp.text}"
                print(err, file=sys.stderr)
                print(err)
                sys.exit(1)
            data = resp.json()
            image_url = data["data"][0]["url"]
            if output_path:
                try:
                    img_resp = requests.get(image_url, timeout=60)
                    with open(output_path, "wb") as f:
                        f.write(img_resp.content)
                    print(f"Image saved to {output_path}")
                except Exception as e:
                    warn = f"Warning: download failed ({e}). URL: {image_url}"
                    print(warn, file=sys.stderr)
                    print(warn)
                    print(image_url)
            else:
                print(image_url)
            return
        except requests.exceptions.Timeout:
            last_error = "timeout"
            if attempt < MAX_RETRIES - 1:
                time.sleep(3)
                continue
        except requests.exceptions.ConnectionError as e:
            last_error = str(e)
            if attempt < MAX_RETRIES - 1:
                time.sleep(5)
                continue
    msg = f"Error: API call failed after {MAX_RETRIES} retries. Last error: {last_error}"
    print(msg, file=sys.stderr)
    print(msg)
    sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate image via Agnes AI API")
    parser.add_argument("--prompt", required=True, help="Image prompt in English")
    parser.add_argument("--size", default="1K", help="Size tier: 1K, 2K, 3K, 4K (recommended) or exact pixels e.g. 1024x768")
    parser.add_argument("--ratio", default=None, help="Aspect ratio: 1:1, 3:4, 4:3, 16:9, 9:16, 2:3, 3:2, 21:9 (default: 1:1)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name")
    parser.add_argument("--output", default=None, help="Output file path")
    args = parser.parse_args()
    generate_image(
        prompt=args.prompt,
        size=args.size,
        ratio=args.ratio,
        model=args.model,
        output_path=args.output,
    )
