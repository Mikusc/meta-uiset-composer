# Layout And Component Patterns

This reference captures the learned structure of Meta XR Interaction SDK UISet samples from:

```text
Runtime/Sample/Objects/UISet/Scenes/UISet.unity
Runtime/Sample/Objects/UISet/Scenes/UISetPatterns.unity
Runtime/Sample/Objects/UISet/Prefabs/**/*.prefab
```

The data was extracted by offline Unity YAML parsing, not by broad Unity MCP component dumps.

## Sample Coverage

`UISet.unity` is the component gallery. Extracted counts:

```text
204 GameObject
286 RectTransform
290 MonoBehaviour
126 CanvasRenderer
86 PrefabInstance
11 CanvasGroup
1 Canvas
1 Light
```

`UISetPatterns.unity` is a pattern gallery. It instantiates these composed prefabs:

```text
ContentUIExample1
ContentUIExample2
ContentUIExample-HorizonOS1
ContentUIExample-HorizonOS2
ContentUIExample-HorizonOS3
ContentUIExample-VideoPlayer
GridMenuExample2x4
GridMenuExample3x3
```

The UISet prefab folder contains these dominant script/component families:

```text
Image, LayoutElement, HorizontalLayoutGroup, VerticalLayoutGroup,
TextMeshProUGUI, RoundedBoxUIProperties, ContentSizeFitter,
PlaneSurface, ClippedPlaneSurface, BoundsClipper,
RectTransformBoundsClipperDriver, Scrollbar, Mask, PointableCanvas,
GraphicRaycaster, RectMask2D, PokeInteractable, RayInteractable,
PointableCanvasUnityEventWrapper, CanvasScaler, Toggle, ScrollRect,
AnimatorOverrideLayerWeigth, Button, CanvasGroupAlphaToggle,
GridLayoutGroup, ToggleGroup, UIThemeManager.
```

## Core Canvas Stack

Use this pattern for a standalone interactive UISet panel:

```text
PanelRoot
  Transform
  PointableCanvas
  PointableCanvasUnityEventWrapper
  AudioSource
  optional UIThemeManager

CanvasRoot
  RectTransform
  Canvas
  CanvasScaler
  GraphicRaycaster
  CanvasRenderer

ISDK_RayInteraction
  RectTransform
  RayInteractable
  LayoutElement(ignoreLayout=1)
  Surface
    RectTransform
    PlaneSurface
    ClippedPlaneSurface
    BoundsClipper
    RectTransformBoundsClipperDriver

ISDK_PokeInteraction
  RectTransform
  PokeInteractable
  LayoutElement(ignoreLayout=1)
  Surface
    RectTransform
    PlaneSurface
    ClippedPlaneSurface
    BoundsClipper
    RectTransformBoundsClipperDriver
```

`EmptyUIBackplateWithCanvas` uses a variant where the root also carries `UIThemeManager`, `PokeInteractable`, `PointableCanvas`, `RayInteractable`, `AudioSource`, and `PointableCanvasUnityEventWrapper`. Its `CanvasRoot` is `500 x 500` and has a `HorizontalLayoutGroup` with `spacing=50`.

When using this prefab as a copied panel shell, preserve the built-in interaction stack for Simulator and Quest testing. The official stack already gives the panel a `PointableCanvas`, ray path, poke path, event wrapper, and surface-backed interaction children. If `meta_add_canvas_interaction_ray` or `meta_add_canvas_interaction_poke` is run on top of this prefab, check for duplicate `ISDK_RayCanvasInteraction` or `ISDK_PokeCanvasInteraction` objects and remove the duplicate rather than removing the prefab's original interaction components.

`UIThemeManager` is not part of the required interaction path. It can be removed when the copied prefab has no valid theme list or logs theme-index warnings, while leaving `PointableCanvas`, `RayInteractable`, `PokeInteractable`, and `PointableCanvasUnityEventWrapper` intact.

## Backplate And Section Stack

Official panel cards use this visual stack:

```text
UIBackplate or Section
  RectTransform
  CanvasRenderer
  Image
  RoundedBoxUIProperties
  Mask
  VerticalLayoutGroup or GridLayoutGroup
  optional CanvasGroup
  optional CanvasGroupAlphaToggle
  optional ContentSizeFitter

GradientEffect or SolidBackplate
  RectTransform stretched anchor 0,0 to 1,1
  LayoutElement(ignoreLayout=1)
  CanvasRenderer
  Image
```

Default card padding and rhythm:

```text
Standard card padding: left/right/top/bottom = 24
Compact tooltip padding: 8
Button internal padding: 12
Normal section spacing: 8 or 12
Large content section spacing: 24
Gallery column spacing: 50
```

Use `RoundedBoxUIProperties` on backplates, button backgrounds, slider tracks, and handles. Use `Mask` when a gradient/backplate needs to clip to the rounded shape.

## Layout Group Grammar

UISet relies on layout groups. Prefer these over manual placement:

```text
VerticalLayoutGroup
  Use for panels, sections, label stacks, form controls.
  Common padding: 24 on cards, 12 inside tile buttons.
  Common spacing: 4 for text input, 8 for compact controls, 12 for rows, 24 for major sections.

HorizontalLayoutGroup
  Use for command rows, label+control rows, icon+text rows, button rows.
  Common spacing: 8 or 12.
  Use childControlWidth=1 for equal or fill rows.
  Use childControlWidth=0 when children should keep fixed preferred widths.

GridLayoutGroup
  Use for tiled menus.
  Cell size: 176 x 100.
  Padding: 24.
  Spacing: 8 x 8.
  Constraint: fixed column count.
  2x4 menu: constraintCount=2.
  3x3 menu: constraintCount=3.

ContentSizeFitter
  Use on generated-size cards and scroll content.
  Grid cards use HorizontalFit=PreferredSize and VerticalFit=PreferredSize.
  Scroll content commonly uses both fits PreferredSize.
```

Unity `m_ChildAlignment` values seen frequently:

```text
0 = UpperLeft
1 = UpperCenter
3 = MiddleLeft
4 = MiddleCenter
```

## Button Patterns

### Command Buttons

`PrimaryButton_IconAndLabel_UnityUIButton` is the base Unity `Button` prefab:

```text
Root: RectTransform 133 x 40 + Button + Animator + HorizontalLayoutGroup
  Content: HorizontalLayoutGroup
    Background: CanvasRenderer + Image + LayoutElement(flexible 1,1) + RoundedBoxUIProperties
      Elements: HorizontalLayoutGroup, middle-centered
        Icon: Image + LayoutElement(preferredWidth=24)
        Gap: LayoutElement(flexibleWidth=1)
        Text: VerticalLayoutGroup, middle-centered
          Label: TextMeshProUGUI
          Subtitle: TextMeshProUGUI
```

Variants are prefab inheritance chains:

```text
SecondaryButton_IconAndLabel_UnityUIButton -> PrimaryButton_IconAndLabel
DestructiveButton_IconAndLabel_UnityUIButton -> SecondaryButton_IconAndLabel
BorderlessButton_IconAndLabel_UnityUIButton -> DestructiveButton_IconAndLabel
```

Use:
- Primary for the one main action in a panel.
- Secondary for preview, accept, inspect, or non-destructive alternatives.
- Destructive for reset/reject/delete.
- Borderless for toolbar-level or low-emphasis actions.

### Toggle-Based Buttons

Toggle button prefabs use:

```text
Root: RectTransform + Toggle + Animator + AnimatorOverrideLayerWeigth
Content: usually VerticalLayoutGroup
Background: Image + LayoutElement(flexible) + RoundedBoxUIProperties
Elements: icon/text stack or switch/checkbox/radio visual
```

Known sizes:

```text
TextTileButton_IconAndLabel_Toggle: 176 x 100
ButtonShelf_IconAndLabel_Toggle: 101 x 72
ToggleButton_Switch: 40 x 24
ToggleButton_Checkbox: 16 x 16
ToggleButton_Radio: 16 x 16
```

Tile button internals:

```text
Content VerticalLayoutGroup: spacing=8, childControlWidth/Height=1
Elements VerticalLayoutGroup: padding=12, icon preferredWidth=24
```

Use tile buttons for theme cards, object categories, or mode choices. Use shelves for compact mode/tool selectors. Use checkbox/switch/radio only when the text label lives in a separate row.

## Sliders

`SmallSlider` is the base slider:

```text
Root: RectTransform 300 x 12 + CanvasRenderer + Slider + Animator
  Background: Image + RoundedBoxUIProperties + Mask, stretched width
    FillOffset: CanvasRenderer
      Fill: Image + RoundedBoxUIProperties
  Handle Slide Area
    Handle: Image + RoundedBoxUIProperties
```

`MediumSlider` and `LargeSlider` inherit from `SmallSlider`.

Label/icon wrappers use:

```text
SmallSlider_LabelsAndIcons: VerticalLayoutGroup, 300 x 24
MediumSliderWithLabelsAndIcons: VerticalLayoutGroup, 300 x 24
LargeSlider_LabelsAndIcons: VerticalLayoutGroup, 300 x 40
LabelsText: HorizontalLayoutGroup, 16 high
LabelsIcon: HorizontalLayoutGroup, 16 high
```

Use sliders for correction magnitude, opacity, scale, height offset, or blend amount. Keep labels outside the slider track wrapper when the panel is dense.

## Text Input And Search

`TextInputField`:

```text
Root: RectTransform 300 x 100 + VerticalLayoutGroup(spacing=4)
  Title: TextMeshProUGUI, 24 high
  TextField: TMP_InputField + Animator, 40 high
    Content
      Background: Image + RoundedBoxUIProperties
    Icon: Image + LayoutElement(preferredWidth=24)
    Text Area
      Placeholder: TextMeshProUGUI + LayoutElement
      Text: TextMeshProUGUI
  HelperText: TextMeshProUGUI, 24 high
```

`SearchBar` inherits from `TextInputField`. Use search only for long lists; for a small MR room dashboard, favor buttons/tabs over search.

## Dropdowns And Context Menus

Dropdown prefabs are built from dropdown list buttons:

```text
DropDownIconAnd2LineText -> 6 x DropDownListButton_IconAndLabel2Lines_Toggle
DropDownIconAnd1LineText -> DropDownIconAnd2LineText + one list button variant
DropDown1LineTextOnly -> DropDownIconAnd1LineText
```

Context menus inherit from dropdowns:

```text
ContextMenu1LineTextOnly -> DropDown1LineTextOnly
ContextMenuIconAnd1LineText -> DropDownIconAnd1LineText
ContextMenuIconAnd2LineText -> DropDownIconAnd2LineText
```

Use dropdowns for many mutually exclusive choices. Use context menus for object-level actions after inspect/select.

## Dialogs

Dialog variants inherit from `Dialog2Button_ImageVideoAndText`:

```text
Dialog2Button_ImageVideoAndText
  2 x PrimaryButton_IconAndLabel
  1 x SecondaryButton_IconAndLabel

Dialog1Button_IconAndText -> Dialog2Button_ImageVideoAndText
Dialog1Button_TextOnly -> Dialog2Button_ImageVideoAndText
Dialog2Button_IconAndText -> Dialog2Button_ImageVideoAndText
Dialog2Button_TextOnly -> Dialog2Button_ImageVideoAndText
```

Use dialogs for accept/reject/reset confirmation. Do not use them for routine theme switching unless the action is destructive.

## Tooltip

`Tooltip`:

```text
Root: RectTransform 314 x 85.7 + CanvasRenderer + VerticalLayoutGroup
  TooltipArrowUp
  Elements: HorizontalLayoutGroup + Image + LayoutElement + RoundedBoxUIProperties
    padding=8, alignment=MiddleLeft
    Icon: Image + LayoutElement 40 x 40
    Space: LayoutElement preferredWidth=8
    Text: VerticalLayoutGroup + LayoutElement(flexibleWidth=160)
      Title: TextMeshProUGUI
      Subtitle: TextMeshProUGUI
  TooltipArrowDown
```

Use tooltips sparingly for unfamiliar icon-only controls. Prefer visible labels for primary MR workflows.

## Pattern Prefabs

Pattern prefabs use the same canvas and interaction stack, then compose reusable UISet prefabs:

```text
GridMenuExample2x4
  CanvasRoot 426.6048 x 493.93335
  GridLayout cell 176 x 100, padding 24, spacing 8, columns=2
  8 x TextTileButton_IconAndLabel_Regular

GridMenuExample3x3
  CanvasRoot 649.65137 x 429.49823
  GridLayout cell 176 x 100, padding 24, spacing 8, columns=3
  9 x TextTileButton_IconAndLabel_Toggle

ContentUIExample-HorizonOS1
  CanvasRoot 1024 x 688
  Backplate VerticalLayoutGroup, padding L24/R12/T24/B24, spacing=24
  Rows use HorizontalLayoutGroup spacing=12
  Scroll View with RectMask2D, ScrollRect, horizontal and vertical Scrollbar
  Content containers use ContentSizeFitter preferred sizing
  25 tile buttons, 10 secondary buttons, 3 borderless buttons, 1 search bar
```

Other pattern composition counts:

```text
ContentUIExample1: 6 shelf toggles, 3 checkboxes, 3 switches, 2 small sliders
ContentUIExample2: 6 text tile regular buttons, 5 secondary buttons
ContentUIExample-HorizonOS2: 15 text tiles, 7 borderless, 8 left-aligned borderless
ContentUIExample-HorizonOS3: 18 text tiles, 3 borderless, 3 left-aligned borderless, 2 dropdowns
ContentUIExample-VideoPlayer: 13 text tiles, 7 borderless, 4 left-aligned borderless, 2 sliders, 1 secondary button
```

## Practical Layout Rules

When building a new panel:

1. Start with a single backplate card, not the full gallery.
2. Use a fixed design width such as 500, 780, 920, or 1024 px, then scale the world-space canvas.
3. Put all primary content inside one `VerticalLayoutGroup`.
4. Use `24 px` padding around cards.
5. Use `24 px` spacing between major sections, `12 px` between rows, `8 px` inside compact controls.
6. Keep command buttons at `40 px` height.
7. Use `176 x 100` tile buttons for theme/category choices.
8. Prefer one primary button per panel row.
9. Put destructive actions away from primary actions, preferably in a confirmation dialog.
10. Use `LayoutElement(ignoreLayout=1)` for stretched background/gradient/interactable surface objects.
11. Stretch background and interaction surfaces with anchors `{0,0}->{1,1}`.
12. Avoid fixed anchored positions except for decorative arrows, scrollbars, or sample-specific title offsets.

For SceneShift, a good dashboard skeleton is:

```text
SceneShiftPanelRoot
  CanvasRoot
    UIBackplate
      Header/status row
      Theme grid or button shelf
      Primary action row: Stylize / Preview
      Correction section: toggle + sliders
      Footer row: Accept / Reset
    ISDK_RayInteraction
    optional ISDK_PokeInteraction
```

Use this control mapping:

```text
Stylize / Apply: PrimaryButton
Preview / Accept: SecondaryButton
Reset / Reject: DestructiveButton or dialog action
Theme choices: TextTileButton or GridMenu
Correction mode: ToggleButton_Switch or ButtonShelf toggle
Nudge/scale/intensity: Slider with labels
Object actions: ContextMenu
Explanations for icon-only actions: Tooltip
```

## What To Avoid

- Do not copy the entire `UISet.unity` gallery into the production scene.
- Do not create nested cards inside cards unless the inner object is a repeated item or dialog.
- Do not manually place every child when a layout group can express the structure.
- Do not let a `UIThemeManager` scope include unrelated project UI.
- Do not duplicate `EventSystem`, `PointableCanvasModule`, `PointableCanvas`, `RayInteractable`, or `PokeInteractable` for the same canvas.
- Do not rely on huge gallery dimensions like `5560 x 1797.92` for an MR dashboard; those are sample-gallery dimensions, not production panel dimensions.
