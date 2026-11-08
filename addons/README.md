# addons/

Self-contained `<script>` blocks that `build.py` injects into the built game just before the boot script.
They are separate from `src/part_*.html`, so they never touch the big game chunks.

## zombie_behind_audio.html
Spatial (HRTF) groans from zombies while they are behind the player.

Sounds: `addons/sounds/behind1.wav` ... `behind5.wav`. build.py base64-embeds every `behind*.wav` there (any count works).
Build: `python build.py` (needs your local assets.json as before) -> omni-ops_built.html

How it works
- Zombies come from `Game.entities` (`e.zombie`, or `e.zproxy` for co-op guests).
- "Behind" = more than ~100 degrees off where the camera looks, for at least 0.3 s.
- Per zombie: one groan, then 3-7.5 s of quiet after the clip ends. Max 3 voices at once, 0.8 s between new ones, nearest zombie first.
- Each voice is a PannerNode (HRTF, inverse distance) that follows the zombie's head every frame; the AudioListener follows the camera.
- Low-passed when a wall is between the zombie and you; cut when the zombie dies. Volume follows the game's master volume setting.

Console (after a match has started)
- `ZombieBehindAudio.test()`  groan 4 m directly behind you;  `.test(6, 90)` 6 m to your right
- `ZombieBehindAudio.sweep()` one groan circling your head (front, right, behind, left)
- `ZombieBehindAudio.cfg` the tunables (maxDist, behindCos, cdMin, cdMax, maxVoices, gain ...)
- `ZombieBehindAudio.debug = true` logs each groan
