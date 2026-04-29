# MCP Playbook

Use this reference when performing Unity MCP or Meta MCP Extension operations for Meta UISet work.

## Safe Read Flow

Start with light reads:

```text
Unity_GetProjectData
Unity_ListResources
Unity_ReadResource
Unity_ReadConsole or Unity_GetConsoleLogs
Unity_ManageScene GetActive/GetBuildSettings/GetHierarchy
```

If Unity recently crashed, prefer filesystem inspection with `rg`, `sed`, and YAML reads until the editor is stable.

## Avoid Broad Component Serialization

Do not use full component dumps on large UISet sample roots such as:

```text
ContentRoot
CanvasRoot
full UISet.unity roots
full UISetPatterns.unity roots
```

Use one of these instead:
- limited hierarchy reads,
- targeted component query on a small known object,
- `Unity_ReadResource` for scripts and assets under `Assets/`,
- direct filesystem YAML inspection for scenes and prefabs,
- package-cache file search for prefab names.

## Meta MCP Extension Flow

Use this sequence for a production world-space UI canvas:

1. Confirm active scene and intended target object.
2. Confirm the target object has a world-space Unity `Canvas`.
3. Run `meta_get_config_information` if available.
4. If the scene lacks a Meta camera rig, run `meta_add_camerarig`.
5. If the scene lacks an interaction rig, run `meta_add_interactionrig`.
6. Add distance interaction with `meta_add_canvas_interaction_ray`.
7. Add near interaction with `meta_add_canvas_interaction_poke` only when required.
8. Run `meta_get_interactors_state` if available.
9. Read console and fix introduced errors before continuing.

`meta_add_canvas_interaction_ray` and `meta_add_canvas_interaction_poke` require a world-space Canvas target.

## Unity Scene Mutation Rules

- Do not load or save scenes casually. Preserve the user's active scene and dirty state.
- Before adding a component, check whether an equivalent component already exists.
- Prefer project-owned prefabs under `Assets/Prefabs/` for customized UI.
- Keep scripts under `Assets/Scripts/UI/` for UI adapters.
- Use small MonoBehaviours with serialized fields for wiring.
- Do not modify packages, Player settings, or XR settings unless the task requires it.

## SceneShift-Specific Checks

For SceneShift-style projects:

```text
Canonical scene: Assets/Scenes/MR_RoomStylization.unity
Existing UI script: Assets/Scripts/UI/SceneShiftUISetDashboard.cs
Build Settings scene: Assets/Scenes/MR_RoomStylization.unity
```

Before changing dashboard UI, inspect `SceneShiftUISetDashboard.cs`. It may intentionally disable inherited UISet runtime components for stability.

## Validation

Minimum validation after changes:

```text
Unity console: no new errors
Target scene: correct active or saved scene
Build settings: canonical scene still present
Hierarchy: one intended UI root, no duplicate EventSystem path
Canvas: world-space, correct size and placement
Interaction: ray/poke components present only where intended
```

For visual work, capture a Scene view or Game view screenshot after Unity is stable. For Quest validation, follow the repository's device validation plan and report exactly what was run.
