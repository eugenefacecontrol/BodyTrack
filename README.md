# Cualigrafía · English / Русский

Standalone bilingual adaptation of the public interactive biomechanics simulations at https://cualigrafia.com/.

36 exercises in English and Russian: three original full simulators, one new multi-segment squat model and 32 educational exercise pages with technique cues and a single-joint lever explorer. Search by name/muscle and filter by group or format. The explorer isolates F × perpendicular moment arm; it is not a complete exercise-specific biomechanical simulation.

## Pages

- `/` and `/ru/index.html` — Russian exercise library.
- `/en/index.html` — English exercise library.
- `prensa.html`, `pendu.html`, `hipo.html` within each language directory — leg press, pendulum squat and hip thrust simulators.
- EN/RU navigation on every page.

The original physics, interactive canvas drawings and explanatory content are adapted from Cualigrafía; credit and a link to the original creator are visible. This is a separate adaptation, not an official translation hosted on the original domain.

## Implementation

Static HTML/CSS/JavaScript. No server, build dependencies, user accounts or email collection. The original mailing-list integration is not connected. Assets in `dist/assets` are embedded source-page posters; simulations render on canvas. Google Fonts is optional, with system-font fallbacks.

`dist/` is the complete deployable site. `.openai/hosting.json` declares the Sites identity and static output directory. Serve `dist/` at the root of any static host.

Regenerate the exercise library with `python expand.py`. Exercise copy is stored in `exercises.tsv`. Run `node test-explorer.cjs` for geometry/control checks.

Run `python validate.py` for local asset/link and script syntax checks. Browser visual QA was unavailable in the authoring environment.

The simplified biomechanical models illustrate trends; they do not measure individual muscle activity.

## Multi-segment squat v1

The barbell squat now has a sagittal linked-segment model, adjustable mass/geometry/load/depth/tempo, dynamic and quasi-static net joint moments, implied ground reaction and required centre of pressure, playback and per-repetition curves. Infeasible poses/contact are flagged. Read [the model assumptions and verification](docs/squat-model.md) before interpreting results: this is prescribed-motion inverse dynamics, not a free-running or experimentally validated muscle simulation.

Run `node test-squat.cjs` and `node test-squat-ui.cjs`. `python expand.py` regenerates both language pages via `build_squat.py`. The GitHub Actions workflow runs all checks before deploying Pages.
