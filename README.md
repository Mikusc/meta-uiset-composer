# Meta UISet Composer

Codex skill for building Quest-ready Unity UI panels from Meta XR Interaction SDK UISet and UISetPatterns examples.

The skill helps Codex:

- choose official Meta UISet prefabs for buttons, toggles, sliders, dialogs, dropdowns, tooltips, grids, and content panels;
- follow learned UISet layout rules from the sample scenes, including padding, spacing, grid sizing, and layout-group usage;
- add world-space canvas ray and poke interaction through Unity MCP and Meta MCP Extension;
- validate saved scenes for Simulator-ready UISet structure without broad MCP component dumps;
- avoid unsafe broad Unity MCP component dumps on large UISet sample roots;
- preserve SceneShift-style MR room stylization workflows without adding unrelated NPC or conversation UI.

## Install

Copy this folder into your Codex skills directory:

```sh
mkdir -p "$CODEX_HOME/skills"
cp -R meta-uiset-composer "$CODEX_HOME/skills/meta-uiset-composer"
```

Then invoke it in Codex:

```text
Use $meta-uiset-composer to build a Quest-ready Meta UISet panel in my Unity scene.
```

## Contents

```text
SKILL.md
agents/openai.yaml
references/uiset-assets-and-scenes.md
references/layout-and-component-patterns.md
references/panel-recipes.md
references/mcp-playbook.md
references/troubleshooting.md
scripts/validate_uiset_scene.py
```

## Notes

This skill references Meta documentation and sample structures, but it is not affiliated with or endorsed by Meta. It does not include Meta SDK assets; your Unity project must have the relevant Meta XR packages installed.

## License

MIT
