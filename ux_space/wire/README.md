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

`apply()`, `pick()`, `orbit()`, `pan()`, and `zoom()` take the handler `ctx` and
require `ctx.verified` to hold a Cap for that verb, so the Soft never becomes ambient.
Verification is Channel's job when the Intent arrives; nothing from `ctx` is copied onto Result ops.

Optional extra: `pip install 'ux-space[channel]'`.
