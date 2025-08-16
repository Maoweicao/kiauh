#!/usr/bin/env python3
"""Translate generated locale JSON files using an OpenAI-compatible API.

Place this script in `kiauh/dev_scripts` and run it from the repo root.

Features:
- Reads `*.generated.json` files from `kiauh/locales`.
- For entries prefixed with '[TO_TRANSLATE] ', calls a configurable API to translate
  the original English text into the target locale.
- Writes final files as `<locale>.json` (no `.generated` suffix) in the same directory.
- API endpoint and API key may be provided via CLI args or environment variables.

Safety:
- Supports `--dry-run` which will not call the API or write files; it prints a summary.
"""

import os
import re
import json
import argparse
import time
from typing import Dict, List, Tuple

try:
    import requests
except Exception:
    requests = None


def locale_filename_from_code(code: str) -> str:
    parts = code.split('-')
    if len(parts) == 1:
        return f"{parts[0]}.json"
    return f"{parts[0].lower()}_{parts[1].upper()}.json"


def load_json(path: str) -> Dict[str, str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def write_json(path: str, data: Dict[str, str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_json_from_text(text: str) -> Dict:
    """Attempt to extract JSON object from a text blob (robust for model outputs)."""
    # Try direct parse first
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        # Fallback: find first {...} substring
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return {}
    return {}


def build_chat_payload(model: str, system_prompt: str, user_prompt: str) -> Dict:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
    }


def translate_batch_openai(api_url: str, api_key: str, model: str, target_locale: str, originals: List[str], verbose: bool = False) -> Dict[str, str]:
    """Call an OpenAI-compatible chat completions endpoint to translate a list of strings.

    Returns mapping original -> translated.
    """
    if requests is None:
        raise RuntimeError('requests library is required to call API')

    system_prompt = "You are a helpful translator."
    # Build a compact JSON-returning instruction
    user_prompt = (
        f"Translate the following English strings into the language for locale '{target_locale}'.\n"
        "Return only a single JSON object that maps each original string to its translation.\n"
        "The keys in the JSON must exactly match the original strings.\n\n"
        "Strings:\n"
    )
    for s in originals:
        # ensure any backticks/newlines don't break the prompt
        user_prompt += f"- {s}\n"

    payload = build_chat_payload(model, system_prompt, user_prompt)

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    if verbose:
        print("[verbose] API URL:", api_url)
        print("[verbose] Request headers:", {k: (v if k != 'Authorization' else 'REDACTED') for k, v in headers.items()})
        print("[verbose] Request payload:", json.dumps(payload, ensure_ascii=False))

    resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
    if verbose:
        print(f"[verbose] Response status: {resp.status_code}")
        # print a bounded amount of response text for safety
        txt = resp.text
        print(f"[verbose] Response text (truncated): {txt[:10000]}")
    if resp.status_code >= 400:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text}")

    data = resp.json()
    # Try common OpenAI response shapes
    content = None
    if isinstance(data, dict):
        # chat completions
        choices = data.get('choices') or data.get('choices', [])
        if choices and isinstance(choices, list):
            first = choices[0]
            if isinstance(first, dict):
                # new format
                msg = first.get('message') or first.get('text') or first.get('delta')
                if isinstance(msg, dict):
                    content = msg.get('content')
                elif isinstance(msg, str):
                    content = msg
                else:
                    content = first.get('text')
        # fallback: raw 'text' field
        if content is None:
            content = data.get('text')

    if content is None:
        # last resort, use full response text
        content = resp.text

    parsed = extract_json_from_text(content)
    # normalize keys
    result: Dict[str, str] = {}
    for k, v in parsed.items():
        if isinstance(v, str):
            result[k] = v
        else:
            result[k] = json.dumps(v, ensure_ascii=False)

    if verbose:
        print(f"[verbose] Parsed translation map contains {len(result)} entries")

    return result


def process_file(generated_path: str, locales_dir: str, api_url: str, api_key: str, model: str, batch_size: int, dry_run: bool, verbose: bool = False):
    print(f"Processing: {generated_path}")
    data = load_json(generated_path)
    if not data:
        print("  empty or unreadable, skipping")
        return

    filename = os.path.basename(generated_path)
    # derive locale filename
    # expected like en_US.generated.json -> en_US.json
    out_filename = filename.replace('.generated.json', '.json')
    out_path = os.path.join(locales_dir, out_filename)

    # Determine locale code from filename (e.g., en_US -> en-US)
    locale_code = out_filename.replace('.json', '')
    locale_code = locale_code.replace('_', '-')

    # collect originals that need translation
    to_translate: List[Tuple[str, str]] = []  # (key, original text)
    for k, v in data.items():
        if isinstance(v, str) and v.startswith('[TO_TRANSLATE] '):
            orig = v[len('[TO_TRANSLATE] '):]
            to_translate.append((k, orig))

    if not to_translate:
        print(f"  no entries to translate for {out_filename}; copying/normalizing file")
        if not dry_run:
            write_json(out_path, data)
        return

    print(f"  {len(to_translate)} entries to translate for {out_filename}")

    translations: Dict[str, str] = {}

    # If locale is English, just strip prefix
    if locale_code.lower().startswith('en'):
        for k, orig in to_translate:
            translations[k] = orig
    else:
        if dry_run:
            # do not call API; simulate
            for k, orig in to_translate:
                translations[k] = f"[SIM_TRANSLATION:{locale_code}] {orig}"
        else:
            # call API in batches
            originals = [orig for _, orig in to_translate]
            keys = [k for k, _ in to_translate]
            for i in range(0, len(originals), batch_size):
                batch = originals[i:i+batch_size]
                # call API
                backoff = 1
                translated_map = {}
                for attempt in range(3):
                    try:
                        translated_map = translate_batch_openai(api_url, api_key, model, locale_code, batch, verbose=verbose)
                        break
                    except Exception as e:
                        print(f"    API call failed (attempt {attempt+1}): {e}")
                        time.sleep(backoff)
                        backoff *= 2

                # map results back to keys
                for j, orig in enumerate(batch):
                    k = keys[i + j]
                    t = translated_map.get(orig)
                    if t:
                        translations[k] = t
                    else:
                        translations[k] = f"[TRANSLATION_FAILED] {orig}"

    # build final map merging translated values with existing non-translated ones
    final_map = dict(data)
    for k, t in translations.items():
        final_map[k] = t

    if dry_run:
        print(f"  dry-run: would write {out_path} with {len(translations)} translated entries")
    else:
        write_json(out_path, final_map)
        print(f"  wrote {out_path}")


def find_generated_files(locales_dir: str, suffix: str = '.generated.json') -> List[str]:
    out = []
    if not os.path.isdir(locales_dir):
        return out
    for name in os.listdir(locales_dir):
        if name.endswith(suffix):
            out.append(os.path.join(locales_dir, name))
    return out


def main():
    parser = argparse.ArgumentParser(description='Translate generated locale JSON files using an OpenAI-like API')
    parser.add_argument('--api-url', help='API URL for chat completions (overrides env OPENAI_API_URL)')
    parser.add_argument('--api-key', help='API key (overrides env OPENAI_API_KEY)')
    parser.add_argument('--model', default='gpt-3.5-turbo', help='Model name to request')
    parser.add_argument('--locales-dir', default=os.path.join(os.path.dirname(__file__), '..', 'locales'), help='Locales directory')
    parser.add_argument('--batch-size', type=int, default=20, help='Number of strings to send per request')
    parser.add_argument('--dry-run', action='store_true', help='Do not call API or write files')
    parser.add_argument('--verbose', action='store_true', help='Print verbose request/response details')
    parser.add_argument('--show-key', action='store_true', help='Show full API key in verbose output (use with caution)')
    args = parser.parse_args()

    api_url = args.api_url or os.environ.get('OPENAI_API_URL') or 'https://api.openai.com/v1/chat/completions'
    api_key = args.api_key or os.environ.get('OPENAI_API_KEY') or ''
    model = args.model

    locales_dir = os.path.abspath(args.locales_dir)

    if not args.dry_run and not api_key:
        print('ERROR: API key required unless --dry-run is used (set OPENAI_API_KEY or pass --api-key)')
        return

    if requests is None and not args.dry_run:
        print('ERROR: requests library is required to call API. Install via pip install requests')
        return

    generated_files = find_generated_files(locales_dir)
    if not generated_files:
        print(f'No generated files found in {locales_dir}')
        return

    if args.verbose:
        displayed_key = api_key if args.show_key else (api_key[:6] + '...' if api_key else '')
        print('[verbose] API settings:')
        print('  api_url:', api_url)
        print('  api_key:', displayed_key)
        print('  model:', model)
        print('  locales_dir:', locales_dir)

    print(f'Found {len(generated_files)} generated files in {locales_dir}')

    for path in generated_files:
        process_file(path, locales_dir, api_url, api_key, model, args.batch_size, args.dry_run, verbose=args.verbose)


if __name__ == '__main__':
    main()
