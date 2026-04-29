# Troubleshooting

Use this reference after scene generation, Play Mode validation, or a Unity crash.

## Error Classification

Treat these as scene/UI issues to fix before delivery:

```text
Theme index out of range
RayInteractable missing Surface
PokeInteractable missing Surface
PointableCanvasModule missing
Duplicate EventSystem
Duplicate ISDK_RayCanvasInteraction over a UISet prefab ray path
Duplicate ISDK_PokeCanvasInteraction over a UISet prefab poke path
FirstPersonLocomotor could not find ground
```

Treat these as common desktop Simulator / OpenXR environment warnings unless paired with broken interaction:

```text
xrGetInstanceProcAddr failed to get function pointer
Local Dimming feature is not supported
XR_ERROR_ACTIONSET_NOT_ATTACHED during startup
unsupported scene capture / room mesh function pointer
```

Do not hide environment warnings in the final summary. State that they were observed and why they do not block UISet structure validation.

## Common Fixes

### Empty UIThemeManager

Symptom:

```text
Theme index out of range
```

Cause: copied UISet prefab or scene contains `UIThemeManager` with `_themes: []`.

Fix: remove that invalid manager or assign valid copied theme assets. Do not remove ray/poke interaction components as part of this fix.

### Missing Surface

Symptom:

```text
RayInteractable missing Surface
PokeInteractable missing Surface
```

Cause: `ISDK_RayInteraction`, `ISDK_PokeInteraction`, or their `Surface` child was deleted while the interactable component remained.

Fix: restore the UISet prefab interaction child stack, or add a complete canvas interaction through Meta MCP Extension if the canvas was hand-built.

### Duplicate Canvas Interaction Helpers

Symptom: two ray or poke paths compete on one canvas, or hierarchy contains extra `ISDK_RayCanvasInteraction` / `ISDK_PokeCanvasInteraction`.

Cause: running `meta_add_canvas_interaction_ray` or `meta_add_canvas_interaction_poke` on a UISet prefab that already had a valid interaction path.

Fix: keep the official UISet prefab interaction stack and remove only the duplicate helper objects.

### Locomotor Ground Warning

Symptom:

```text
FirstPersonLocomotor could not find ground
```

Cause: comprehensive interaction rig includes locomotion in an otherwise empty test scene.

Fix: add a simple non-trigger ground collider below the rig in Simulator scenes, or configure locomotion intentionally for the target scene.

### Duplicate Camera Path

Symptom: a standalone preview `Main Camera` coexists with `OVRCameraRig`.

Fix: for Simulator/Quest scenes, keep `OVRCameraRig` as the XR camera entry and remove standalone preview cameras. A temporary preview camera is acceptable only before adding the Meta camera rig.

## Delivery Checklist

Before final response:
- target scene path is named,
- Unity console error count is reported,
- warnings are classified as scene/UI or environment,
- Build Settings impact is reported,
- Simulator-ready status is reported,
- Quest/device validation status is reported separately,
- created and modified files are listed,
- next smallest follow-up is stated.
