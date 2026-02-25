#!/usr/bin/env python
"""
collect_skills.py — Aggregate Claude Code skills from multiple sources.

Sources:
  1. Non-dot subfolders in this repo  (SKILL.md, *.md with frontmatter, PDFs via AI)
  2. All public repos of a GitHub user (default: dirkpetersen)
     — copies from .claude/skills/ folders and SKILL.md files anywhere in the repo
  3. URLs listed in skills.txt
     — fetches SKILL.md from the direct folder at each URL

Rules enforced (from "The Complete Guide to Building Skills for Claude"):
  - YAML frontmatter delimited by --- (required)
  - name:  kebab-case, no spaces, no capitals, no "claude"/"anthropic" prefix
  - description: includes WHAT it does AND WHEN to use it; specific trigger phrases
  - No XML angle brackets (< >) anywhere — security restriction
  - Keep under ~5 000 words per skill file

Usage:
  python3 collect_skills.py [options]

Options:
  --dry-run             Show what would happen without writing files
  -v, --verbose         Extra output
  --github-user NAME    GitHub user to scan (default: dirkpetersen)
  --source {local,github,urls} [...]
                        One or more sources to collect from (default: all three)
  --no-generate         Disable skill generation from PDF/text docs
                        Generation is ON by default when 'claude' CLI is in PATH
                        or ANTHROPIC_API_KEY is set (CLI takes priority).
                        When using the CLI, PDFs are read natively — no extra library needed.
                        SDK fallback needs: pip install pymupdf4llm anthropic
  --overwrite           Replace skills that already exist in .claude/skills/

GitHub rate limits:
  Unauthenticated: 60 req/h.  Set GH_TOKEN or GITHUB_TOKEN env var for 5 000 req/h.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── paths ──────────────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).resolve().parent
SKILLS_DIR  = REPO_ROOT / ".claude" / "skills"
SKILLS_TXT  = REPO_ROOT / "skills.txt"

GITHUB_API_BASE = "https://api.github.com"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"


# ── GitHub helpers ─────────────────────────────────────────────────────────────

def _github_headers() -> dict:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "collect-skills/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _github_get(url: str) -> Optional[dict | list]:
    req = urllib.request.Request(url, headers=_github_headers())
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        if exc.code == 403:
            print(f"    WARNING: GitHub rate-limit hit. Set GH_TOKEN for higher quota.")
            return None
        raise
    except urllib.error.URLError as exc:
        print(f"    WARNING: network error fetching {url}: {exc}")
        return None


def _fetch_raw(url: str) -> Optional[str]:
    req = urllib.request.Request(url, headers={"User-Agent": "collect-skills/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None


# ── YAML frontmatter helpers ───────────────────────────────────────────────────

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (metadata_dict, body).  Values are raw strings (no YAML library needed)."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    yaml_block = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    meta: dict = {}
    for line in yaml_block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def is_valid_skill(content: str) -> bool:
    """Quick validity check: needs --- delimiters, name, and description."""
    meta, _ = parse_frontmatter(content)
    name = meta.get("name", "")
    desc = meta.get("description", "")
    if not name or not desc:
        return False
    # name must be kebab-case (no spaces, no upper case)
    if re.search(r"[A-Z \t]", name):
        return False
    # no XML angle brackets (security rule from the guide)
    if "<" in content or ">" in content:
        # Allow markdown code fences containing < > only inside ``` blocks
        # Simple heuristic: reject if < or > appears outside code blocks
        stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        stripped = re.sub(r"`[^`]+`", "", stripped)
        if "<" in stripped or ">" in stripped:
            return False
    return True


def sanitize_name(name: str) -> str:
    """Convert any string to a valid kebab-case skill name."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = name.strip("-")
    name = re.sub(r"-+", "-", name)
    # Guard against reserved prefixes
    for prefix in ("claude-", "anthropic-"):
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name or "unnamed-skill"


def skill_dirname(meta: dict, fallback: str) -> str:
    """Return the kebab-case directory name for a skill."""
    return sanitize_name(meta.get("name") or fallback)


# Skills that always get their own top-level folder even when found inside
# another repo's .claude/skills/ — they are generic, not repo-specific.
GENERIC_SKILLS = {
    "bash", "zsh", "fish", "python", "javascript", "typescript", "nodejs",
    "go", "rust", "java", "ruby", "php", "c", "cpp", "csharp", "swift",
    "kotlin", "sql", "git", "docker", "kubernetes", "terraform", "ansible",
}


# ── install helper ─────────────────────────────────────────────────────────────

def install_skill(
    content: str,
    skill_dir: str,
    dry_run: bool,
    verbose: bool,
    overwrite: bool,
    filename: str = "SKILL.md",
) -> bool:
    dest = SKILLS_DIR / skill_dir / filename
    label = f"{skill_dir}/{filename}"
    if dest.exists() and not overwrite:
        if verbose:
            print(f"    (skip — {label} already exists; use --overwrite to replace)")
        return False
    if dry_run:
        action = "overwrite" if dest.exists() else "create"
        print(f"    [dry-run] would {action} {dest}")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    if verbose:
        print(f"    -> written {dest}")
    # When placing a skill as a sub-file (e.g. appmotel/traefik.md), remove
    # the now-redundant standalone directory (e.g. traefik/SKILL.md).
    if filename != "SKILL.md":
        standalone = SKILLS_DIR / Path(filename).stem / "SKILL.md"
        if standalone.exists():
            standalone.unlink()
            if verbose:
                print(f"    -> removed standalone {standalone.relative_to(SKILLS_DIR)}")
            try:
                standalone.parent.rmdir()   # succeeds only if dir is now empty
            except OSError:
                pass
    return True


def _append_see_also(skill_dir: str, sub_files: list[str]) -> None:
    """Add a ## See Also section to skill_dir/SKILL.md if not already present."""
    skill_file = SKILLS_DIR / skill_dir / "SKILL.md"
    if not skill_file.exists():
        return
    content = skill_file.read_text(encoding="utf-8")
    if "## See Also" in content:
        return
    links = "\n".join(
        f"- [{f.removesuffix('.md').replace('-', ' ').title()}]({f})"
        for f in sorted(sub_files)
    )
    skill_file.write_text(content.rstrip() + f"\n\n## See Also\n\n{links}\n", encoding="utf-8")


def _migrate_flat_skills(dry_run: bool, verbose: bool) -> None:
    """Move any legacy .claude/skills/name.md  →  .claude/skills/name/SKILL.md"""
    for md in sorted(SKILLS_DIR.glob("*.md")):
        skill_name = md.stem
        dest = SKILLS_DIR / skill_name / "SKILL.md"
        if dest.exists():
            if verbose:
                print(f"  [migrate] {md.name} already at {skill_name}/SKILL.md — removing flat file")
            if not dry_run:
                md.unlink()
            continue
        print(f"  [migrate] {md.name} -> {skill_name}/SKILL.md")
        if not dry_run:
            dest.parent.mkdir(exist_ok=True)
            md.rename(dest)


# ── Source 1: local subfolders ─────────────────────────────────────────────────

def collect_local(dry_run: bool, verbose: bool, generate: bool, overwrite: bool) -> None:
    print("\n=== Source 1: local subfolders ===")
    for item in sorted(REPO_ROOT.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        if verbose:
            print(f"  Scanning {item.name}/")

        installed = False

        # 1-a  explicit SKILL.md  (official format used by claude.ai)
        for candidate in (item / "SKILL.md", item / "skill.md"):
            if candidate.exists():
                content = candidate.read_text(encoding="utf-8")
                if is_valid_skill(content):
                    meta, _ = parse_frontmatter(content)
                    sdir = skill_dirname(meta, item.name)
                    print(f"  [local] {item.name}/{candidate.name} -> {sdir}/SKILL.md")
                    install_skill(content, sdir, dry_run, verbose, overwrite)
                    installed = True
                    break

        # 1-b  any *.md with valid YAML frontmatter
        if not installed:
            for md in sorted(item.glob("*.md")):
                if md.name.upper() == "README.MD":
                    continue  # skip plain READMEs unless they have frontmatter
                content = md.read_text(encoding="utf-8", errors="replace")
                if is_valid_skill(content):
                    meta, _ = parse_frontmatter(content)
                    sdir = skill_dirname(meta, item.name)
                    print(f"  [local] {item.name}/{md.name} -> {sdir}/SKILL.md")
                    install_skill(content, sdir, dry_run, verbose, overwrite)
                    installed = True
                    break

        # 1-c  PDFs
        #   - claude CLI available: pass pdf_path directly (CLI reads PDFs natively)
        #   - SDK fallback: extract text first with pymupdf4llm / pypdf / pdftotext
        if not installed and generate:
            claude_bin = shutil.which("claude")
            for pdf in sorted(item.rglob("*.pdf")):
                if pdf.name.endswith(":Zone.Identifier"):
                    continue
                if claude_bin:
                    skill_content = _generate_skill_via_claude(None, item.name, pdf_path=pdf)
                else:
                    text = _extract_pdf_text(pdf)
                    if not text:
                        continue
                    skill_content = _generate_skill_via_claude(text, item.name)
                if skill_content and is_valid_skill(skill_content):
                    meta, _ = parse_frontmatter(skill_content)
                    sdir = skill_dirname(meta, item.name)
                    print(f"  [local+AI] {item.name}/{pdf.name} -> {sdir}/SKILL.md")
                    install_skill(skill_content, sdir, dry_run, verbose, overwrite)
                    installed = True
                    break

        if not installed and verbose:
            print(f"    (nothing usable found in {item.name}/)")


def _extract_pdf_text(pdf_path: Path) -> Optional[str]:
    """Try pymupdf4llm → pypdf → pdftotext CLI."""
    try:
        import pymupdf4llm  # pip install pymupdf4llm
        return pymupdf4llm.to_markdown(str(pdf_path))
    except ImportError:
        pass
    except Exception as exc:
        print(f"    WARNING: pymupdf4llm failed on {pdf_path.name}: {exc}")

    try:
        from pypdf import PdfReader  # pip install pypdf
        reader = PdfReader(str(pdf_path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        pass
    except Exception as exc:
        print(f"    WARNING: pypdf failed on {pdf_path.name}: {exc}")

    try:
        result = subprocess.run(
            ["pdftotext", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    print(
        f"    WARNING: cannot extract text from {pdf_path.name}.\n"
        f"             Install one of: pymupdf4llm, pypdf, or poppler-utils (pdftotext)."
    )
    return None


def _generate_skill_via_claude(
    doc_text: Optional[str],
    folder_name: str,
    pdf_path: Optional[Path] = None,
) -> Optional[str]:
    """
    Generate a skill file from documentation.

    Primary path  — `claude` CLI in batch mode (`-p` flag):
      Uses the first `claude` found in PATH, which may be a ~/bin wrapper that
      configures AWS Bedrock credentials.  When pdf_path is supplied the CLI reads
      the PDF natively via its built-in Read tool — no extraction library needed.

    Fallback path — Anthropic Python SDK:
      Used when `claude` is not in PATH (e.g. GitHub Actions).
      Requires ANTHROPIC_API_KEY and extracted doc_text.
    """
    skill_name = sanitize_name(folder_name)

    instructions = f"""Output ONLY the raw skill file — no preamble, no commentary, nothing else.

STRICT FORMAT RULES:
1. First line must be exactly:  ---
2. Then:  name: {skill_name}
3. Then a verbose description field (see DESCRIPTION RULES below)
4. Then:  ---
5. Then the Markdown body

DESCRIPTION RULES — model the official Anthropic style exactly:
- Start with "Use this skill whenever the user wants to..."
- Exhaustively list EVERY task, sub-task, file extension, command, API, concept, and
  natural-language phrase that should trigger this skill.
- Include what NOT to use it for if relevant ("Do NOT use for simple X").
- Aim for 3-6 sentences / 400-900 characters.  No XML angle brackets anywhere.

BODY RULES:
- Sections: ## Setup, ## Quick Start, ## Examples, ## Key Concepts, ## References
- Every code example must use a fenced block with a language tag (python, bash, go, etc.)
- NO XML tags anywhere (no angle brackets outside code fences) — security requirement
- Keep the total file under 5 000 words
- ## References: link to every official doc URL mentioned in the source material"""

    # ── primary: claude CLI ────────────────────────────────────────────────────
    claude_bin = shutil.which("claude")
    if claude_bin:
        if pdf_path:
            prompt = (
                f"Read the PDF at {pdf_path} and create a Claude Code skill file "
                f"for it with the name '{skill_name}'.\n\n{instructions}"
            )
        else:
            doc_excerpt = (doc_text or "")[:14000]
            prompt = (
                f"Create a Claude Code skill file named '{skill_name}' from "
                f"this documentation:\n\n{doc_excerpt}\n\n{instructions}"
            )
        try:
            result = subprocess.run(
                [claude_bin, "-p", prompt],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            print(f"    WARNING: claude CLI non-zero exit: {result.stderr[:200]}")
        except Exception as exc:
            print(f"    WARNING: claude CLI error: {exc}")
        # fall through to SDK

    # ── fallback: Anthropic Python SDK ─────────────────────────────────────────
    if not doc_text:
        return None  # nothing to send to the SDK

    try:
        import anthropic  # pip install anthropic
    except ImportError:
        print("    WARNING: 'anthropic' package not installed. Run: pip install anthropic")
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("    WARNING: ANTHROPIC_API_KEY not set and claude CLI unavailable.")
        return None

    full_prompt = (
        f"Create a Claude Code skill file named '{skill_name}' from "
        f"this documentation:\n\n{doc_text[:14000]}\n\n{instructions}"
    )
    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": full_prompt}],
        )
        return msg.content[0].text.strip()
    except Exception as exc:
        print(f"    WARNING: Anthropic SDK error: {exc}")
        return None


# ── Source 2: GitHub user repos ────────────────────────────────────────────────

THIS_REPO = "claude-skills"   # skip — it is the target repo


def collect_github_user(
    username: str, dry_run: bool, verbose: bool, overwrite: bool
) -> None:
    print(f"\n=== Source 2: GitHub user '{username}' ===")

    # Paginate through all public repos
    repos: list[dict] = []
    page = 1
    while True:
        url = (
            f"{GITHUB_API_BASE}/users/{username}/repos"
            f"?per_page=100&page={page}&type=public"
        )
        batch = _github_get(url)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    print(f"  Found {len(repos)} public repos")

    cutoff = datetime.now(timezone.utc).timestamp() - 30 * 86400

    for repo in repos:
        repo_name: str = repo["name"]
        if repo_name == THIS_REPO:
            if verbose:
                print(f"  Skipping {repo_name} (target repo)")
            continue
        pushed_at = repo.get("pushed_at") or ""
        if pushed_at:
            pushed_ts = datetime.fromisoformat(pushed_at.replace("Z", "+00:00")).timestamp()
            if pushed_ts < cutoff:
                if verbose:
                    print(f"  Skipping {repo_name} (no activity in 30 days)")
                continue
        branch: str = repo.get("default_branch", "main")
        if verbose:
            print(f"  Checking {repo_name} [{branch}] …")

        # Fetch the full file tree (recursive) — one API call per repo
        tree_url = (
            f"{GITHUB_API_BASE}/repos/{username}/{repo_name}"
            f"/git/trees/{branch}?recursive=1"
        )
        tree_data = _github_get(tree_url)
        if not tree_data or "tree" not in tree_data:
            continue

        blobs: list[str] = [
            item["path"]
            for item in tree_data["tree"]
            if item.get("type") == "blob"
        ]

        repo_key = sanitize_name(repo_name)
        dot_skills_paths = [
            p for p in blobs
            if p.startswith(".claude/skills/") and p.endswith(".md")
        ]
        installed_paths: set[str] = set()

        # 2-a  .claude/skills/*.md — collect first, then group by repo
        if dot_skills_paths:
            # Fetch all skills from this repo's .claude/skills/
            fetched: dict[str, tuple[dict, str]] = {}   # stem -> (meta, content)
            for path in dot_skills_paths:
                raw = f"{GITHUB_RAW_BASE}/{username}/{repo_name}/{branch}/{path}"
                content = _fetch_raw(raw)
                if content and is_valid_skill(content):
                    meta, _ = parse_frontmatter(content)
                    fetched[Path(path).stem] = (meta, content)

            # Identify the primary skill (name matches the repo)
            primary_stem = next(
                (s for s, (m, _) in fetched.items()
                 if sanitize_name(m.get("name") or s) == repo_key),
                None,
            )

            sub_files_installed: list[str] = []

            for stem, (meta, content) in fetched.items():
                skill_name = sanitize_name(meta.get("name") or stem)
                is_primary = (stem == primary_stem)
                is_generic = skill_name in GENERIC_SKILLS

                if is_primary:
                    target_dir, target_file = repo_key, "SKILL.md"
                elif primary_stem and not is_generic:
                    # Sub-skill: lives inside the primary skill's folder
                    target_dir  = repo_key
                    target_file = f"{skill_name}.md"
                    sub_files_installed.append(target_file)
                else:
                    # Generic / standalone skill — own top-level folder
                    target_dir, target_file = skill_name, "SKILL.md"

                print(f"  [github:{repo_name}] .claude/skills/{stem}.md -> {target_dir}/{target_file}")
                install_skill(content, target_dir, dry_run, verbose, overwrite, filename=target_file)
                installed_paths.add(f".claude/skills/{stem}.md")

            # Link sub-files from the primary SKILL.md
            if sub_files_installed and not dry_run:
                _append_see_also(repo_key, sub_files_installed)

        # 2-b  SKILL.md files anywhere in the repo (outside .claude/skills/)
        for path in blobs:
            if Path(path).name == "SKILL.md" and path not in installed_paths:
                raw = f"{GITHUB_RAW_BASE}/{username}/{repo_name}/{branch}/{path}"
                content = _fetch_raw(raw)
                if content and is_valid_skill(content):
                    meta, _ = parse_frontmatter(content)
                    folder = Path(path).parent.name or repo_name
                    sdir = skill_dirname(meta, folder)
                    print(f"  [github:{repo_name}] {path} -> {sdir}/SKILL.md")
                    install_skill(content, sdir, dry_run, verbose, overwrite)


# ── Source 3: skills.txt URLs ──────────────────────────────────────────────────

def collect_from_urls(dry_run: bool, verbose: bool, overwrite: bool) -> None:
    print("\n=== Source 3: skills.txt URLs ===")
    if not SKILLS_TXT.exists():
        print("  skills.txt not found — skipping")
        return

    lines = SKILLS_TXT.read_text(encoding="utf-8").splitlines()
    urls = [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]

    for url in urls:
        print(f"  Checking: {url}")
        raw_skill_url = _resolve_skill_md_url(url)
        if not raw_skill_url:
            if verbose:
                print(f"    (could not resolve SKILL.md URL for {url})")
            continue

        if verbose:
            print(f"    -> fetching {raw_skill_url}")
        content = _fetch_raw(raw_skill_url)

        if content and is_valid_skill(content):
            meta, _ = parse_frontmatter(content)
            fallback = Path(urllib.parse.urlparse(url).path).name or "unnamed"
            sdir = skill_dirname(meta, fallback)
            print(f"  [url] {url} -> {sdir}/SKILL.md")
            install_skill(content, sdir, dry_run, verbose, overwrite)
        else:
            if verbose:
                reason = "invalid frontmatter" if content else "not found"
                print(f"    (SKILL.md {reason} at {raw_skill_url})")


def _resolve_skill_md_url(url: str) -> Optional[str]:
    """
    Given a URL (GitHub tree page or plain https URL), return the raw URL
    for the SKILL.md file in that directory.

    Handles:
      https://github.com/owner/repo/tree/branch/path/to/folder
      https://github.com/owner/repo                          (root)
      https://github.com/owner/repo/blob/branch/SKILL.md    (direct)
      https://example.com/some/path/                         (append SKILL.md)
    """
    # 1. GitHub tree URL  →  raw.githubusercontent.com/.../SKILL.md
    m = re.match(
        r"https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/?(.*)",
        url,
    )
    if m:
        owner, repo, branch, path = m.groups()
        path = path.rstrip("/")
        folder = f"{path}/" if path else ""
        return f"{GITHUB_RAW_BASE}/{owner}/{repo}/{branch}/{folder}SKILL.md"

    # 2. GitHub blob URL pointing directly at SKILL.md
    m = re.match(
        r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*/SKILL\.md)",
        url,
    )
    if m:
        owner, repo, branch, path = m.groups()
        return f"{GITHUB_RAW_BASE}/{owner}/{repo}/{branch}/{path}"

    # 3. Root of a GitHub repo  →  check main then master
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/?$", url)
    if m:
        owner, repo = m.groups()
        for branch in ("main", "master"):
            raw = f"{GITHUB_RAW_BASE}/{owner}/{repo}/{branch}/SKILL.md"
            if _fetch_raw(raw) is not None:
                return raw
        return None

    # 4. raw.githubusercontent.com URL — use as-is or append SKILL.md
    if "raw.githubusercontent.com" in url:
        if url.endswith("SKILL.md"):
            return url
        return url.rstrip("/") + "/SKILL.md"

    # 5. Generic URL — just append SKILL.md
    return url.rstrip("/") + "/SKILL.md"


# ── CLI ────────────────────────────────────────────────────────────────────────

class _HelpOnErrorParser(argparse.ArgumentParser):
    """Print full help (not just a terse error) on any argument mistake."""
    def error(self, message: str) -> None:
        self.print_help(sys.stderr)
        sys.stderr.write(f"\nerror: {message}\n")
        sys.exit(2)


def main(argv: Optional[list[str]] = None) -> int:
    parser = _HelpOnErrorParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would happen without writing any files",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Extra output",
    )
    parser.add_argument(
        "--github-user", default="dirkpetersen", metavar="NAME",
        help="GitHub username to scan (default: dirkpetersen)",
    )
    parser.add_argument(
        "--source", nargs="+", choices=["local", "github", "urls"],
        metavar="SOURCE",
        help="Sources to collect from: local github urls (default: all three)",
    )
    parser.add_argument(
        "--no-generate", action="store_true",
        help=(
            "Disable auto-generation of skill files from PDF/text docs. "
            "Generation is ON by default when 'claude' CLI is in PATH or "
            "ANTHROPIC_API_KEY is set."
        ),
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Overwrite skill files that already exist in .claude/skills/",
    )
    args = parser.parse_args(argv)

    # flag omitted → default None → run all three
    sources = set(args.source) if args.source else {"local", "github", "urls"}

    # claude CLI takes priority; SDK is the GitHub Actions fallback
    claude_bin = shutil.which("claude")
    generate = (bool(claude_bin) or bool(os.environ.get("ANTHROPIC_API_KEY"))) and not args.no_generate

    print("Claude Skills Collector")
    print(f"  repo root : {REPO_ROOT}")
    print(f"  skills dir: {SKILLS_DIR}")
    if args.dry_run:
        print("  *** DRY RUN — no files will be written ***")
    if generate:
        if claude_bin:
            print(f"  AI generation: ON  (claude CLI: {claude_bin})")
        else:
            print("  AI generation: ON  (Anthropic SDK fallback, ANTHROPIC_API_KEY set)")
    else:
        if args.no_generate:
            reason = "--no-generate flag"
        else:
            reason = "no 'claude' in PATH and ANTHROPIC_API_KEY not set"
        print(f"  AI generation: OFF  ({reason})")

    _migrate_flat_skills(args.dry_run, args.verbose)

    if "local" in sources:
        collect_local(args.dry_run, args.verbose, generate, args.overwrite)

    if "github" in sources:
        collect_github_user(
            args.github_user, args.dry_run, args.verbose, args.overwrite
        )

    if "urls" in sources:
        collect_from_urls(args.dry_run, args.verbose, args.overwrite)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
