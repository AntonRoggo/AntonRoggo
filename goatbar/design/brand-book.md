GoatBar makes protein bars for people who spend their weekends outside. The brand looks like good mountain gear: clean, quiet and premium, with the mountains doing the talking. Real alpine light, cold air, a gold larch in autumn. Never gym-bro, never neon.

## Voice

- Short, plain sentences. Say what is in the bar and what it is for: "20 g protein. 6 ingredients. Made for the climb."
- Confident, never loud. No exclamation marks, no emoji, no "beast mode".
- The name is written GoatBar (one word, capital G and B). The site is GoatBar.co.
- Mountain facts are content, not decoration: real elevations, coordinates and route names, set in `data`.

## Colour

- Ground is `snow`; text is `ink`, secondary text `ink-muted`. Cards and nutrition panels sit on `snow-raised` with a `line` hairline, no shadows.
- `spruce` is the brand: the wrapper field, the wordmark, primary buttons (label in `on-spruce`).
- `larch` is the only warm colour. Use it once per layout: the sun on the pack, a protein callout, a sale tag. Text on it is `on-larch`.
- `glacier` and `rock` build mountain scenes: far ridges in `glacier`, near peaks in `rock`, layered back to front.
- Never gradients. Depth comes from stacked flat ridges, like a screen print.

## Type

- Headlines in `display` and `headline` (Archivo at font-stretch 125%), sentence case. One `display` line per layout.
- `label` is the only uppercase style: eyebrows, pack labels, buttons.
- Reading text in `body` (Instrument Sans), product names in `title`.
- Numbers that come from the mountains or the label (grams, metres, coordinates, batch numbers) are `data` in IBM Plex Mono.

## Shapes and pattern

- Corners are square (`radius-none`) everywhere except buttons (`radius-sm`) and tags (`radius-full`).
- The pattern is topographic contour lines: a few hairlines in `line` on snow, or in `on-spruce` at low weight on spruce, spaced at `space-l`. Never a dense field.
- Mountains are flat silhouettes in two or three layers (`glacier` behind `rock`, with `larch` for the sun). No outlines, no textures.
- Leave room: outer margins at `space-xl`, at least a third of any layout empty.

## Photography

- Real mountains, real people outside, early or late light. The bar appears in use: in a pocket, on a rock, in a gloved hand.
- Natural colour, slightly cool. No studio sweeps, no fake sweat, no gym.

## Packaging

- The wrapper is a `spruce` field with the mountain scene across the bottom third, the wordmark top left, the flavour name in `display`.
- Each flavour is named after a real peak or place and carries its elevation in `data` (for example "4,158 m").
- Protein grams sit in a `larch` tag. Ingredients and macros sit on the back on `snow-raised`.

## Instagram

- The grid alternates three tiles: a mountain photo, a flat-colour post (`spruce` or `snow` ground with one `headline`), and the bar in use outdoors.
- Text on posts: one headline and at most one line of `body`. Logo small, bottom left.

## Logo

- There is no logo yet. Until there is, set GoatBar in `headline` (Archivo, wide, weight 700) in `spruce`.
