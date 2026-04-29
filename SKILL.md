---
name: meta-uiset-composer
description: Use when designing, composing, modifying, or validating Meta Quest Unity UI built from Meta XR Interaction SDK UISet or UISetPatterns examples, especially with Unity MCP and Meta MCP Extension world-space canvas setup, ray/poke interaction, QDS theming, and SceneShift MR room stylization dashboards.
---

# Meta UISet Composer

## Purpose

Build Quest-ready Unity UI panels from Meta XR Interaction SDK UISet examples while preserving project conventions, official Meta tooling, and Unity MCP safety.

Use this skill for:
- Composing UI from Meta UISet/UISetPatterns sample prefabs.
- Adding world-space canvas interaction through Meta MCP Extension.
- Wiring MR dashboard controls to existing project components.
- Debugging UISet, PointableCanvas, ray, poke, theme, or EventSystem issues.

## Load References

Load only what the task needs:
- `references/uiset-assets-and-scenes.md` for UISet package paths, sample scene structure, prefab choices, and QDS theme notes.
- `references/layout-and-component-patterns.md` for learned component stacks, script mounting patterns, and official UISet layout rules from `UISet.unity` and `UISetPatterns.unity`.
- `references/panel-recipes.md` for reusable dashboard, inspector, theme picker, dialog, and debug panel layouts.
- `references/mcp-playbook.md` for Unity MCP and Meta MCP Extension command flow, validation, and known crash-avoidance rules.
- `references/troubleshooting.md` for known UISet, Simulator, OpenXR, theme, ray/poke, and delivery checklist issues.

Bundled script:
- `scripts/validate_uiset_scene.py` checks a Unity scene YAML plus referenced prefabs for Simulator-ready UISet structure without broad Unity MCP component dumps.

## Preflight

Before editing a Unity project:
1. Read the repo's agent instructions and required docs.
2. Inspect package state, project structure, scene list, build settings, and console.
3. Confirm the target scene. For SceneShift, default to `Assets/Scenes/MR_RoomStylization.unity`.
4. Avoid package changes unless the user asked for them or the required official package is truly missing.
5. If Unity has just crashed or MCP feels unstable, use filesystem/YAML inspection first and postpone scene mutation.

For SceneShift, preserve the current product direction: MR room stylization, preview, correction, accept/reject/reset, and theme switching. Do not add NPC or conversational-agent UI.

## UI Contract

Define the UI contract before creating objects:
- Placement: head-relative, room-anchored, wall/table anchored, or object anchored.
- Interaction: ray, poke, or both.
- Controls: buttons, toggles, sliders, menus, dialogs, status fields.
- Runtime wiring: target MonoBehaviours, serialized fields, UnityEvents, and fallback states.
- Safety states: room unavailable, no plan, apply failed, correction active, reset pending.

For SceneShift's vertical slice, prefer controls for:
- room-ready and semantic status,
- theme selection,
- preview/stylize/apply,
- correction mode,
- reset/reject/accept,
- debug/status details.

## UISet Selection

Prefer official UISet assets over hand-rolled styling.

Start from:
- `EmptyUIBackplateWithCanvas` for a clean panel shell.
- `PrimaryButton_IconAndLabel_UnityUIButton` for main commands.
- `SecondaryButton_IconAndLabel_UnityUIButton` for secondary commands.
- `DestructiveButton_IconAndLabel_UnityUIButton` for reset/reject actions.
- `ToggleButton_Switch`, `ToggleButton_Checkbox`, or `ToggleButton_Radio` for binary and option state.
- `SmallSlider`, `MediumSlider`, or `LargeSlider` for correction intensity, scale, and offset controls.
- Dialog prefabs for destructive confirmation or accept/reject flows.
- Grid/content pattern prefabs only when the panel needs a dense menu or media layout.

For panel layout, follow the learned UISet grammar: fixed world-space canvas, backplate card, 24 px outer padding, 8/12/24 px spacing, stable 40 px command rows, 176 x 100 px tile buttons, and layout groups instead of manual absolute positioning. See `references/layout-and-component-patterns.md`.

Do not edit assets under `Library/PackageCache`. If customization is required, copy selected prefabs/materials/themes into project-owned folders such as `Assets/Prefabs/`, `Assets/Materials/`, or `Assets/Data/`.

## Composition Workflow

1. Create or reuse a dedicated UI root for the feature.
2. Ensure the panel uses a world-space `Canvas`.
3. Keep exactly one effective EventSystem/`PointableCanvasModule` path.
4. Add or verify Meta camera and interaction rigs only if the scene is missing them.
5. Add `PointableCanvas`, ray interaction, and poke interaction only to the intended canvas.
6. Wire UI controls through small adapter scripts under `Assets/Scripts/UI/`.
7. Keep style data in ScriptableObjects or serializable project data, not in scene-only hardcoded branches.
8. Validate console, hierarchy, and bundled script output after each change set when filesystem scene YAML is available.

For Meta MCP Extension canvas setup:
- Use `meta_add_canvas_interaction_ray` for distance selection.
- Use `meta_add_canvas_interaction_poke` for near-field hand/controller interaction.
- The target GameObject must already have a world-space Unity `Canvas`.
- For Simulator or Quest validation, ray and poke paths are part of the expected runtime contract. Do not remove `PointableCanvas`, `RayInteractable`, `PokeInteractable`, `PointableCanvasUnityEventWrapper`, or the interaction rig just because a physical headset is unavailable.
- If a copied UISet prefab already includes valid ray/poke interactables and their surface children, verify them instead of blindly adding duplicate canvas interaction objects.

## SceneShift Defaults

When working in this repository:
- Canonical scene: `Assets/Scenes/MR_RoomStylization.unity`.
- Existing UI adapter to respect: `Assets/Scripts/UI/SceneShiftUISetDashboard.cs`.
- Existing package samples may appear as `Assets/Scenes/UISet.unity` and `Assets/Scenes/UISetPatterns.unity`.
- Simulator-first panels should include the same interaction-facing components expected on device: `OVRCameraRig`, an Interaction SDK rig, `PointableCanvas`, `RayInteractable`, `PokeInteractable`, and `PointableCanvasUnityEventWrapper` where the UISet prefab provides them.
- Only remove inherited sample-only managers when they are demonstrably invalid in the copied prefab or scene. A common example is `UIThemeManager` copied with an empty theme list that logs `Theme index out of range`.
- Disable ray/poke components only for an explicitly visual-only fallback, and state that the scene is not interaction-complete until the components are restored.

## MCP Safety

Avoid full component dumps on large UISet roots. In particular, do not call broad component serialization on `ContentRoot`, full `CanvasRoot`, or whole UISet sample scenes. Use narrow hierarchy queries, targeted component checks, or file/YAML inspection instead.

This matters because large UISet sample roots can contain deep references and theme/interaction graphs that may hang or crash the Unity Editor during MCP serialization.

## Validation

At minimum:
- Read Unity console after changes.
- Confirm target scene and build settings.
- Confirm the intended canvas is world-space.
- Confirm ray/poke interactors exist only once per intended canvas.
- Run `scripts/validate_uiset_scene.py <scene> --project-root <unity-project>` when validating a saved scene from disk.
- Run a scene or camera capture when visual layout matters and Unity is stable.
- If Quest/device validation is requested, follow the project's device validation docs and state what was actually run.

If Unity crashed or was not reopened, say that Unity-side validation was not completed and describe the filesystem checks that were completed.
