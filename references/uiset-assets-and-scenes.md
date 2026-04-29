# UISet Assets And Scenes

Use this reference when choosing official Meta UISet sources or interpreting sample scene structure.

For detailed component stacks, script mounting, and layout rules learned from the scenes and prefabs, also read `layout-and-component-patterns.md`.

## Official Documentation

- UISet overview: https://developers.meta.com/horizon/documentation/unity/unity-isdk-uiset/
- Create UI with Interaction SDK: https://developers.meta.com/horizon/documentation/unity/unity-isdk-create-ui-overview/
- Create UISet UI: https://developers.meta.com/horizon/documentation/unity/unity-isdk-create-uiset-ui/
- Meta MCP Extension: https://developers.meta.com/horizon/documentation/unity/unity-mcp-extension/

## Discover Package Paths

Package cache hashes vary. Discover local paths with:

```sh
rg --files Library/PackageCache | rg 'UISet|PointableCanvas|CurvedUnityCanvas|FlatUnityCanvas'
```

Example Interaction SDK UISet package cache path:

```text
Library/PackageCache/com.meta.xr.sdk.interaction@<hash>/Runtime/Sample/Objects/UISet
```

Known compatible package family from inspected SceneShift projects:

```text
com.meta.xr.sdk.core 201.0.0
com.meta.xr.sdk.interaction 201.0.0
com.meta.xr.sdk.interaction.ovr 201.0.0
com.meta.xr.mrutilitykit 201.0.0
com.meta.xr.unity-mcp.extension 2.0.0-pre.2
```

## Sample Scenes

`Scenes/UISet.unity` demonstrates a full UI component gallery:

```text
PointableCanvasModule
Directional Light
ContentRoot
  CanvasRoot
  ThemeButtons
  UIBackplate & TypeRamp
  Buttons
  Controls & DropDown
  Sliders & TextField & Tooltip
  Dialogs
  ISDK_PokeInteraction
Quad (inactive)
```

Important components seen on the full sample:
- `EventSystem` plus `PointableCanvasModule` on `PointableCanvasModule`.
- World-space UGUI canvas, `GraphicRaycaster`, and `CanvasScaler` under `CanvasRoot`.
- `RayInteractable`, `PokeInteractable`, `PointableCanvas`, `UIThemeManager`, and `PointableCanvasUnityEventWrapper` around the sample content root.

`Scenes/UISetPatterns.unity` demonstrates composed layouts:

```text
PointableCanvasModule
Directional Light
ContentRoot
  GridMenuExample2x4
  GridMenuExample3x3
  ContentUIExample1
  ContentUIExample2
  ContentUIExample-HorizonOS1
  ContentUIExample-HorizonOS2
  ContentUIExample-HorizonOS3
ContentUIExample-VideoPlayer
```

Do not copy whole sample scenes into production scenes unless the task explicitly asks for a sample gallery. Copy only the needed prefabs or reproduce the pattern in project-owned prefabs.

## Prefab Catalog

Common starting points:

```text
Prefabs/Backplate/EmptyUIBackplateWithCanvas.prefab
Prefabs/Button/UnityUIButtonBased/PrimaryButton_IconAndLabel_UnityUIButton.prefab
Prefabs/Button/UnityUIButtonBased/SecondaryButton_IconAndLabel_UnityUIButton.prefab
Prefabs/Button/UnityUIButtonBased/DestructiveButton_IconAndLabel_UnityUIButton.prefab
Prefabs/Button/UnityUIToggleBased/ButtonShelf_IconAndLabel_Toggle.prefab
Prefabs/Button/UnityUIToggleBased/TextTileButton_IconAndLabel_Toggle.prefab
Prefabs/Button/UnityUIToggleBased/ToggleButton_Checkbox.prefab
Prefabs/Button/UnityUIToggleBased/ToggleButton_Radio.prefab
Prefabs/Button/UnityUIToggleBased/ToggleButton_Switch.prefab
Prefabs/Slider/SmallSlider.prefab
Prefabs/Slider/MediumSlider.prefab
Prefabs/Slider/LargeSlider.prefab
Prefabs/DropDown/DropDownIconAnd1LineText.prefab
Prefabs/Dialog/Dialog1Button_TextOnly.prefab
Prefabs/Dialog/Dialog2Button_TextOnly.prefab
Prefabs/Tooltip/Tooltip.prefab
Prefabs/TextInputField/SearchBar.prefab
Prefabs/TextInputField/TextInputField.prefab
Prefabs/Patterns/GridMenuExample2x4.prefab
Prefabs/Patterns/GridMenuExample3x3.prefab
```

Canvas props:

```text
com.meta.xr.sdk.interaction/.../Runtime/Sample/Objects/Props/FlatUnityCanvas.prefab
com.meta.xr.sdk.interaction.ovr/.../Runtime/Sample/Objects/Props/CurvedUnityCanvas.prefab
```

## Themes And Tags

UISet theming uses `UIThemeManager`, `UITheme` assets, and QDS tag components. Common tags include:

```text
QDSUIBackplateGradient
QDSUIIcon
QDSUISharedThemeColor
QDSUIPrimaryButton
QDSUIToggleButton
```

Known theme assets:

```text
Themes/UIThemeQuest_Dark.asset
Themes/UIThemeQuest_Light.asset
Themes/UIThemeCustomBrandExample1.asset
Themes/UIThemeCustomBrandExample2.asset
```

Keep theme managers scoped to the UI subtree they should own. Copy theme assets into `Assets/` before customizing colors, fonts, or materials.

## Practical Pitfalls

- Avoid duplicate `EventSystem` or duplicate `PointableCanvasModule`.
- Avoid duplicate `PointableCanvas`, `RayInteractable`, or `PokeInteractable` on the same canvas.
- UISet sample scale can be very small, around `0.0005`; verify final real-world dimensions.
- QDS tags can recolor more than intended if a theme manager is scoped too high.
- Package cache assets are not project-owned; do not edit them in place.
