#!/usr/bin/env python3
"""
MyTake CLI — command-line interface for power users.

Usage examples:
  python cli.py list
  python cli.py process "The factory pattern is..."
  python cli.py process https://youtube.com/watch?v=xxx
  python cli.py show 3
  python cli.py show 3 --section my_simple
  python cli.py stats
  python cli.py voice
  python cli.py export --output ./my-export
"""

import sys
import json
import argparse
import asyncio
from pathlib import Path
from datetime import datetime

# Add backend root to path so "app" imports work
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.storage.database import init_db, AsyncSessionLocal
from app.storage.repository import ContentRepository, VoiceFeedbackRepository
from app.ai.claude import ClaudeClient
from app.extractors.content import ContentExtractor
from app.storage.markdown import MarkdownGenerator
from app.voice.profile import VoiceProfile


# ── helpers ──────────────────────────────────────────────────────────────────

def hr(char="─", width=72):
    print(char * width)


# ── commands ─────────────────────────────────────────────────────────────────

async def cmd_process(args):
    extractor = ContentExtractor()
    claude = ClaudeClient()

    print(f"  extracting ({args.type})…")
    extracted = extractor.extract(args.input, args.type)
    print(f"  ✓ {extracted['title'][:70]}")

    print("  generating 4-part analysis…")
    t0 = datetime.utcnow()
    analysis = claude.generate_four_part_analysis(
        content_text=extracted["text"],
        title=extracted.get("title", "Untitled"),
        source_type=extracted["source_type"],
    )
    elapsed = (datetime.utcnow() - t0).total_seconds()
    print(f"  ✓ done in {elapsed:.1f}s")

    async with AsyncSessionLocal() as session:
        content_data = {
            "url": extracted.get("url"),
            "source_type": extracted["source_type"],
            "title": extracted.get("title", "Untitled"),
            "original_text": extracted["text"],
            "what_they_said_deep": analysis["what_they_said_deep"],
            "what_they_said_simple": analysis["what_they_said_simple"],
            "what_i_say_simple": analysis["what_i_say_simple"],
            "what_i_say_deep": analysis["what_i_say_deep"],
            "voice_profile_version": analysis["voice_profile_version"],
            "processing_time_seconds": analysis["processing_time_seconds"],
        }
        content = await ContentRepository.create(session, content_data)
        await session.commit()

        md_path = MarkdownGenerator.create_and_save(content.to_dict())
        await ContentRepository.update(session, content.id, {"markdown_path": md_path})
        await session.commit()

        hr()
        print(f"  saved  →  ID {content.id}   {md_path}")
        hr()


async def cmd_show(args):
    SECTION_MAP = {
        "deep":      ("What they said — deep",    "what_they_said_deep"),
        "simple":    ("What they said — simple",  "what_they_said_simple"),
        "my_simple": ("What I'd say — simple",    "what_i_say_simple"),
        "my_deep":   ("What I'd say — deep",      "what_i_say_deep"),
    }

    async with AsyncSessionLocal() as session:
        c = await ContentRepository.get_by_id(session, args.id)
        if not c:
            print(f"No content with ID {args.id}")
            return

        hr("═")
        print(f"  ID {c.id}  ·  {c.source_type.upper()}  ·  {c.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"  {c.title[:70]}")
        hr("═")

        sections = (
            [SECTION_MAP[args.section]]
            if args.section
            else SECTION_MAP.values()
        )

        for label, attr in sections:
            print(f"\n## {label}\n")
            print(getattr(c, attr))
            print()
            hr()


async def cmd_list(args):
    async with AsyncSessionLocal() as session:
        items = await ContentRepository.get_all(session, limit=args.limit)

    if not items:
        print("No content yet — run: python cli.py process <url-or-text>")
        return

    print(f"\n{'ID':<5} {'Type':<10} {'Date':<12} {'Secs':>5}  Title")
    hr()
    for c in items:
        secs = f"{c.processing_time_seconds:.1f}" if c.processing_time_seconds else "  —"
        title = c.title[:55] + "…" if len(c.title) > 55 else c.title
        print(f"{c.id:<5} {c.source_type:<10} {c.created_at.strftime('%Y-%m-%d'):<12} {secs:>5}  {title}")


async def cmd_stats(args):
    async with AsyncSessionLocal() as session:
        items = await ContentRepository.get_all(session, limit=10000)
        all_feedback = []
        for c in items:
            all_feedback.extend(await VoiceFeedbackRepository.get_by_content_id(session, c.id))

    if not items:
        print("No content yet.")
        return

    times = [c.processing_time_seconds for c in items if c.processing_time_seconds]
    by_type: dict = {}
    for c in items:
        by_type[c.source_type] = by_type.get(c.source_type, 0) + 1

    positive = sum(1 for f in all_feedback if f.sounds_like_me == 1)

    print("\n📊  MyTake Statistics")
    hr()
    print(f"  Total processed   {len(items)}")
    print(f"  Avg process time  {sum(times)/len(times):.2f}s" if times else "  Avg process time  —")
    print(f"  Min / Max time    {min(times):.2f}s / {max(times):.2f}s" if times else "")
    print()
    print("  Content types:")
    for k, v in sorted(by_type.items()):
        print(f"    {k:<12} {v}")
    print()
    if all_feedback:
        pct = positive / len(all_feedback) * 100
        print(f"  Voice feedback    {len(all_feedback)} total  ({pct:.0f}% positive)")
    else:
        print("  Voice feedback    none yet")
    hr()


async def cmd_export(args):
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    async with AsyncSessionLocal() as session:
        items = await ContentRepository.get_all(session, limit=10000)

    for c in items:
        fname = f"{c.id:04d}_{c.created_at.strftime('%Y%m%d')}_{c.source_type}.json"
        (out / fname).write_text(json.dumps(c.to_dict(), indent=2, default=str))

    print(f"✓ Exported {len(items)} items → {out}/")


def cmd_voice(args):
    vp = VoiceProfile()
    p = vp.export_profile()
    print("\n🎭  Voice Profile")
    hr()
    print(f"  Version      {p['version']}")
    print(f"  Updated      {p['updated_at'][:19]}")
    print()
    print("  Style:")
    for k, v in p["style_rules"].items():
        print(f"    {k:<22} {v}")
    print()
    print("  Traits:")
    for t in p["personality_traits"]:
        print(f"    • {t}")
    print()
    print("  Learning:")
    print(f"    Positive examples     {len(p['learning']['positive_examples'])}")
    print(f"    Feedback incorporated {len(p['learning']['feedback_incorporated'])}")
    hr()


# ── main ─────────────────────────────────────────────────────────────────────

async def async_main():
    await init_db()

    parser = argparse.ArgumentParser(
        prog="mytake",
        description="MyTake CLI — process content & manage your voice profile",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="COMMAND")

    # process
    p = sub.add_parser("process", help="Process a URL or text snippet")
    p.add_argument("input", help="URL or text to process")
    p.add_argument("-t", "--type",
                   choices=["auto", "youtube", "tiktok", "text"],
                   default="auto", help="Force content type (default: auto)")

    # show
    p = sub.add_parser("show", help="Show a processed item by ID")
    p.add_argument("id", type=int)
    p.add_argument("-s", "--section",
                   choices=["deep", "simple", "my_simple", "my_deep"],
                   default=None, help="Show only one section")

    # list
    p = sub.add_parser("list", help="List recent items")
    p.add_argument("-n", "--limit", type=int, default=20)

    # stats
    sub.add_parser("stats", help="Show processing statistics")

    # export
    p = sub.add_parser("export", help="Export all items as JSON")
    p.add_argument("-o", "--output", default="export", metavar="DIR")

    # voice
    sub.add_parser("voice", help="Show current voice profile")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return

    dispatch = {
        "process": cmd_process,
        "show":    cmd_show,
        "list":    cmd_list,
        "stats":   cmd_stats,
        "export":  cmd_export,
        "voice":   lambda a: cmd_voice(a) or asyncio.sleep(0),
    }

    try:
        result = dispatch[args.cmd](args)
        if asyncio.iscoroutine(result):
            await result
    except KeyboardInterrupt:
        print("\nAborted.")
    except Exception as e:
        print(f"❌  {e}")
        if "--debug" in sys.argv:
            raise


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
