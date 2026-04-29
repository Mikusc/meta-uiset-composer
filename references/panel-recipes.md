# Panel Recipes

Use these recipes when the user asks for a complete Meta UISet panel rather than a one-off control.

## SceneShift Stylization Dashboard

Use for MR room stylization preview, correction, accept/reject/reset, or theme switching.

```text
PanelRoot
  CanvasRoot
    UIBackplate
    ContentRoot
      Header
        title, subtitle, selected-theme/status pill
      ThemePresetStrip
        2-4 TextTileButton_IconAndLabel_Toggle
      PanelBody
        SemanticSummaryColumn
          compact status rows for MRUK, perception, planner, correction
        AdjustmentColumn
          sliders, switches, inspect/correction controls
      ActionRow
        Preview secondary button
        Apply primary button
        Reset destructive button
```

Layout targets:
- world-space size around `900 x 640` px for a dashboard panel,
- 24 px outer padding,
- 18-24 px major spacing,
- 12 px row/control spacing,
- fixed 40-56 px command rows,
- 176 x 100 px theme tiles.

Required states:
- room unavailable,
- room ready,
- no plan,
- preview active,
- correction active,
- apply succeeded,
- reset/reject pending.

## Object Inspector / Correction Panel

Use for a selected anchor, furniture proxy, or generated candidate.

```text
Header: selected semantic label + source/confidence
ObjectSummary: original role, proposed replacement, collision sensitivity
TransformControls: nudge/rotate/scale sliders or steppers
DecisionRow: Accept, Reject, Reset Object
```

Keep this panel smaller than the dashboard. Do not include theme browsing here; link back to the main dashboard state instead.

## Theme Picker

Use tile buttons with a `ToggleGroup`.

```text
ThemeGrid or ThemeStrip
  TextTileButton_IconAndLabel_Toggle x N
Footer
  Preview secondary button
  Apply primary button
```

Theme tiles should show the theme name and one short functional hint, not long explanatory copy.

## Confirmation Dialog

Use UISet dialog prefabs for destructive or irreversible actions.

```text
Dialog
  Title
  Short consequence text
  Secondary cancel button
  Destructive confirm button
```

Use confirmation for full reset, reject all, or replacing accepted room styling. Do not confirm every small correction nudge.

## Debug Status Panel

Use when the task is diagnostics rather than end-user flow.

```text
StatusHeader
Counters
  MRUK anchors
  perception records
  fusion records
  plan entries
LogList
  compact last events / warnings
ActionRow
  Refresh, Export, Clear
```

Keep debug panels dense and scannable. Avoid hero layouts, large decorative imagery, and long instructions.
