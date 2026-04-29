#!/usr/bin/env python3
"""Heuristic Unity YAML validator for Meta UISet scene readiness.

This script is intentionally text-based so it can run even when Unity MCP is
unstable. Pair it with Unity Console validation before calling a scene done.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


SCRIPT_RE = re.compile(
    r"--- !u!114 &(?P<file_id>-?\d+)\nMonoBehaviour:\n(?P<body>.*?)(?=\n--- !u!|\Z)",
    re.S,
)
SCRIPT_GUID_RE = re.compile(r"m_Script: \{fileID: 11500000, guid: ([0-9a-f]+), type: 3\}")
PREFAB_BLOCK_RE = re.compile(
    r"--- !u!1001 &-?\d+\nPrefabInstance:\n(?P<body>.*?)(?=\n--- !u!|\Z)", re.S
)
SOURCE_PREFAB_RE = re.compile(r"m_SourcePrefab: \{fileID: 100100000, guid: ([0-9a-f]+), type: 3\}")
REMOVED_COMPONENT_RE = re.compile(r"- \{fileID: (-?\d+), guid: ([0-9a-f]+), type: 3\}")
CANVAS_WORLDSPACE_RE = re.compile(r"--- !u!223 &-?\d+\nCanvas:\n(?P<body>.*?)(?=\n--- !u!|\Z)", re.S)


@dataclass
class Check:
    status: str
    name: str
    detail: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def iter_meta_files(project_root: Path) -> Iterable[Path]:
    roots = [project_root / "Assets", project_root / "Packages", project_root / "ProjectSettings"]
    package_cache = project_root / "Library" / "PackageCache"
    if package_cache.exists():
        roots.append(package_cache)

    for root in roots:
        if not root.exists():
            continue
        for current, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in {".git", "Temp", "Logs", "obj"}]
            for file_name in files:
                if file_name.endswith(".meta"):
                    yield Path(current) / file_name


def build_guid_index(project_root: Path) -> Tuple[Dict[str, Path], Dict[str, str]]:
    assets: Dict[str, Path] = {}
    scripts: Dict[str, str] = {}

    for meta in iter_meta_files(project_root):
        try:
            head = read_text(meta)[:300]
        except OSError:
            continue
        match = re.search(r"^guid: ([0-9a-f]+)$", head, re.M)
        if not match:
            continue
        guid = match.group(1)
        asset_path = meta.with_suffix("")
        assets[guid] = asset_path
        if asset_path.suffix == ".cs":
            scripts[guid] = asset_path.stem

    return assets, scripts


def prefab_removed_components(scene_text: str) -> Dict[str, Set[str]]:
    removed: Dict[str, Set[str]] = {}
    for block in PREFAB_BLOCK_RE.finditer(scene_text):
        body = block.group("body")
        source = SOURCE_PREFAB_RE.search(body)
        if not source:
            continue
        source_guid = source.group(1)
        for file_id, guid in REMOVED_COMPONENT_RE.findall(body):
            if guid == source_guid:
                removed.setdefault(guid, set()).add(file_id)
    return removed


def referenced_prefabs(scene_text: str) -> Set[str]:
    return set(SOURCE_PREFAB_RE.findall(scene_text))


def resolve_prefab_texts(
    root_text: str,
    assets_by_guid: Dict[str, Path],
    removed_by_guid: Dict[str, Set[str]],
) -> List[Tuple[str, str, Set[str]]]:
    queue = list(referenced_prefabs(root_text))
    seen: Set[str] = set()
    texts: List[Tuple[str, str, Set[str]]] = []

    while queue:
        guid = queue.pop()
        if guid in seen:
            continue
        seen.add(guid)
        path = assets_by_guid.get(guid)
        if not path or path.suffix != ".prefab" or not path.exists():
            continue
        text = read_text(path)
        texts.append((str(path), text, removed_by_guid.get(guid, set())))
        for nested_guid in referenced_prefabs(text):
            if nested_guid not in seen:
                queue.append(nested_guid)

    return texts


def component_counts(text: str, script_guid_to_class: Dict[str, str], removed_file_ids: Set[str]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for match in SCRIPT_RE.finditer(text):
        file_id = match.group("file_id")
        if file_id in removed_file_ids:
            continue
        script_match = SCRIPT_GUID_RE.search(match.group("body"))
        if not script_match:
            continue
        class_name = script_guid_to_class.get(script_match.group(1), "UnknownMonoBehaviour")
        counts[class_name] = counts.get(class_name, 0) + 1
    return counts


def add_counts(total: Dict[str, int], extra: Dict[str, int]) -> None:
    for key, value in extra.items():
        total[key] = total.get(key, 0) + value


def count_worldspace_canvas(texts: Iterable[str]) -> int:
    count = 0
    for text in texts:
        for match in CANVAS_WORLDSPACE_RE.finditer(text):
            if re.search(r"m_RenderMode: 2\b", match.group("body")):
                count += 1
    return count


def names_in_text(texts: Iterable[str], name: str) -> int:
    total = 0
    for text in texts:
        total += len(re.findall(rf"^\s*m_Name: {re.escape(name)}$", text, re.M))
        total += len(re.findall(rf"^\s*value: {re.escape(name)}$", text, re.M))
    return total


def explicit_m_name_count(text: str, name: str) -> int:
    return len(re.findall(rf"^\s*m_Name: {re.escape(name)}$", text, re.M))


def editor_build_settings(project_root: Path) -> str:
    path = project_root / "ProjectSettings" / "EditorBuildSettings.asset"
    if not path.exists():
        return ""
    return read_text(path)


def check_required(checks: List[Check], name: str, ok: bool, detail: str, visual_only: bool = False) -> None:
    if ok:
        checks.append(Check("pass", name, detail))
    elif visual_only:
        checks.append(Check("warn", name, f"{detail}; visual-only fallback accepted"))
    else:
        checks.append(Check("fail", name, detail))


def validate(args: argparse.Namespace) -> Tuple[List[Check], Dict[str, int]]:
    project_root = Path(args.project_root).resolve()
    scene_path = Path(args.scene)
    if not scene_path.is_absolute():
        scene_path = project_root / scene_path

    if not scene_path.exists():
        return [Check("fail", "scene file", f"missing scene: {scene_path}")], {}

    scene_text = read_text(scene_path)
    assets_by_guid, script_guid_to_class = build_guid_index(project_root)
    removed_by_guid = prefab_removed_components(scene_text)
    prefab_texts = resolve_prefab_texts(scene_text, assets_by_guid, removed_by_guid)
    all_texts = [scene_text] + [text for _, text, _ in prefab_texts]

    counts: Dict[str, int] = {}
    add_counts(counts, component_counts(scene_text, script_guid_to_class, set()))
    for _, text, removed in prefab_texts:
        add_counts(counts, component_counts(text, script_guid_to_class, removed))

    checks: List[Check] = []
    visual_only = bool(args.visual_only)

    check_required(
        checks,
        "OVRCameraRig",
        names_in_text([scene_text], "OVRCameraRig") >= 1,
        "scene should contain one Meta camera rig for Simulator/Quest interaction",
        visual_only,
    )
    if explicit_m_name_count(scene_text, "Main Camera") > 0 and names_in_text([scene_text], "OVRCameraRig") > 0:
        checks.append(Check("warn", "standalone Main Camera", "standalone Main Camera coexists with OVRCameraRig"))

    check_required(
        checks,
        "Interaction SDK rig",
        names_in_text([scene_text], "OVRInteractionComprehensive") >= 1,
        "scene should contain OVRInteractionComprehensive under the camera rig",
        visual_only,
    )
    check_required(
        checks,
        "world-space canvas",
        count_worldspace_canvas(all_texts) >= 1,
        "at least one Canvas should use RenderMode.WorldSpace",
        visual_only,
    )
    check_required(
        checks,
        "EventSystem input",
        counts.get("PointableCanvasModule", 0) >= 1 or counts.get("StandaloneInputModule", 0) >= 1,
        "scene should have an EventSystem input module; PointableCanvasModule is preferred",
        visual_only,
    )

    for class_name in ("PointableCanvas", "PointableCanvasUnityEventWrapper", "RayInteractable", "PokeInteractable"):
        check_required(
            checks,
            class_name,
            counts.get(class_name, 0) >= 1,
            f"{class_name} should exist for Simulator/Quest UI interaction",
            visual_only,
        )

    if counts.get("RayInteractable", 0) > 1:
        checks.append(Check("warn", "duplicate RayInteractable", f"found {counts['RayInteractable']} RayInteractable components"))
    if counts.get("PokeInteractable", 0) > 1:
        checks.append(Check("warn", "duplicate PokeInteractable", f"found {counts['PokeInteractable']} PokeInteractable components"))

    if names_in_text(all_texts, "ISDK_RayCanvasInteraction") > 0:
        checks.append(Check("warn", "duplicate ray canvas helper", "ISDK_RayCanvasInteraction is present; verify it is not duplicated over UISet's built-in ray path"))
    if names_in_text(all_texts, "ISDK_PokeCanvasInteraction") > 0:
        checks.append(Check("warn", "duplicate poke canvas helper", "ISDK_PokeCanvasInteraction is present; verify it is not duplicated over UISet's built-in poke path"))

    if counts.get("UIThemeManager", 0) > 0 and "_themes: []" in "\n".join(all_texts):
        checks.append(Check("warn", "empty UIThemeManager", "UIThemeManager appears with an empty theme list; remove or assign valid themes"))

    if args.expected_build_scene:
        settings = editor_build_settings(project_root)
        expected = args.expected_build_scene.replace("\\", "/")
        current_scene = str(scene_path.relative_to(project_root)).replace("\\", "/")
        if expected in settings:
            checks.append(Check("pass", "build settings", f"expected build scene present: {expected}"))
        else:
            checks.append(Check("warn", "build settings", f"expected build scene not found: {expected}"))
        if current_scene != expected and current_scene in settings:
            checks.append(Check("warn", "build settings sandbox", f"test scene is included in Build Settings: {current_scene}"))

    return checks, counts


def print_human(checks: List[Check], counts: Dict[str, int]) -> None:
    for check in checks:
        print(f"[{check.status.upper()}] {check.name}: {check.detail}")
    interesting = [
        "PointableCanvasModule",
        "PointableCanvas",
        "PointableCanvasUnityEventWrapper",
        "RayInteractable",
        "PokeInteractable",
        "UIThemeManager",
    ]
    print("\nComponent counts:")
    for name in interesting:
        print(f"- {name}: {counts.get(name, 0)}")


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", help="Unity scene path, absolute or project-root relative")
    parser.add_argument("--project-root", default=".", help="Unity project root")
    parser.add_argument("--expected-build-scene", default="", help="Expected canonical Build Settings scene")
    parser.add_argument("--visual-only", action="store_true", help="Downgrade interaction-readiness failures to warnings")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args(argv)

    checks, counts = validate(args)
    failed = any(check.status == "fail" for check in checks)

    if args.json:
        print(json.dumps({"checks": [check.__dict__ for check in checks], "counts": counts}, indent=2))
    else:
        print_human(checks, counts)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
