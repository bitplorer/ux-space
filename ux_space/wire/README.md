# wire/

Isolation door. **Off** the top-level `ux_space.__all__`.

Product code that must speak Channel imports **here** (or a compose
`wire/` door) — never `ux_channel` from `core/`, `features/`, or app
modules.

## KEEP — do not invent a second Cap Host

| Channel owns | This door |
|--------------|-----------|
| Cap mint (`CapService.mint` / `ch.control`) | Forwards; never HMAC-signs |
| `Channel.boot` | `ux_space.wire.boot` when `ux-channel` is installed |
| `mount_channel` | `ux_space.wire.mount_channel` pass-through |
| Intent verify | Not reimplemented |

`apply()`, `pick()`, `orbit()`, `pan()`, and `zoom()` still require a Cap token so the Soft never becomes ambient.
The token stays on the server — it is not copied onto Result ops.
Verification is Channel's job when the Intent arrives.

Optional extra: `pip install 'ux-space[channel]'`.
