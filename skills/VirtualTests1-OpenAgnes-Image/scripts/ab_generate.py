import subprocess
import sys
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATE_SCRIPT = os.path.join(SCRIPT_DIR, "generate.py")


def _variant_b_prompt(prompt_a):
    """Generate a semantically varied version of the prompt for B testing."""
    swaps = {
        "real photograph": ["authentic photograph", "genuine photo", "real-life shot"],
        "natural lighting": ["ambient lighting", "available light", "diffused light"],
        "detailed": ["intricate", "elaborate", "refined"],
        "high quality": ["premium quality", "exceptional quality"],
        "beautiful": ["stunning", "gorgeous", "breathtaking"],
        "soft": ["gentle", "subtle", "delicate"],
        "vibrant": ["lively", "rich", "saturated"],
        "clean": ["pristine", "pure", "uncluttered"],
        "atmospheric": ["evocative", "ambient", "mood-enhanced"],
    }
    words = prompt_a.split()
    result = []
    swapped_any = False
    for w in words:
        clean_w = w.strip(".,!?;:")
        if clean_w in swaps:
            replacement = random.choice(swaps[clean_w])
            result.append(w.replace(clean_w, replacement))
            swapped_any = True
        else:
            result.append(w)
    if not swapped_any:
        result.append(", cinematic composition")
    return " ".join(result)


def run_variant(prompt, size, ratio, model, output_path):
    cmd = [sys.executable, GENERATE_SCRIPT]
    cmd.extend(["--prompt", prompt])
    if size:
        cmd.extend(["--size", size])
    if ratio:
        cmd.extend(["--ratio", ratio])
    if model:
        cmd.extend(["--model", model])
    if output_path:
        cmd.extend(["--output", output_path])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.returncode != 0:
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
            return False, result.stderr or "unknown error"
        return True, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="A/B test two prompt variants")
    parser.add_argument("--prompt", required=True, help="Base prompt (variant A)")
    parser.add_argument("--size", default="1K", help="Size tier: 1K, 2K, 3K, 4K or exact pixels")
    parser.add_argument("--ratio", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--output-a", default="variant_a.png")
    parser.add_argument("--output-b", default="variant_b.png")
    args = parser.parse_args()

    prompt_a = args.prompt
    prompt_b = _variant_b_prompt(prompt_a)

    print("=" * 50)
    print("Variant A prompt:")
    print(f"  {prompt_a}")
    print("=" * 50)
    print("Variant B prompt:")
    print(f"  {prompt_b}")
    print("=" * 50)

    print("\n--- Generating Variant A ---")
    ok_a, msg_a = run_variant(
        prompt_a, args.size, args.ratio, args.model, args.output_a
    )
    print(f"Variant A: {'OK' if ok_a else 'FAILED'}")
    if not ok_a:
        print(f"  Error: {msg_a}")

    print("\n--- Generating Variant B ---")
    ok_b, msg_b = run_variant(
        prompt_b, args.size, args.ratio, args.model, args.output_b
    )
    print(f"Variant B: {'OK' if ok_b else 'FAILED'}")
    if not ok_b:
        print(f"  Error: {msg_b}")

    print("\n" + "=" * 50)
    if ok_a and ok_b:
        print(f"Variant A: {args.output_a}")
        print(f"Variant B: {args.output_b}")
        print("\nPresent both images to the user and ask which they prefer.")
    elif ok_a:
        print(f"Only Variant A succeeded: {args.output_a}")
    elif ok_b:
        print(f"Only Variant B succeeded: {args.output_b}")
    else:
        print("Both variants failed. Check the errors above.")
    print("=" * 50)
