# GoatBar (GoatBar.co)

Anton's own e-commerce brand: a protein bar for people who spend their weekends outside. Early stage: building the design language, then the bar, packaging, website and Instagram.

## Start here

| For | Open |
|---|---|
| Anything visual (pack, site, posts, ads) | Design language: https://claude.ai/artifact/JUbTWeusarw33cJbAoXxjg (read its `project/README.md` and `project/tokens.json` with the Artifact tool). Git mirror: `design/` |
| Figma file (where Anton designs) | https://www.figma.com/design/E3umMGnl44LGyUojFyGfgx (file key `E3umMGnl44LGyUojFyGfgx`). Pages: Design language (board + Swatch component), Designs (sections Packaging, Website, Instagram with empty artboards), References (one section per reference folder) |
| Design references Anton likes | `references/catalog.json` (files in Dropbox `/[08] GoatBar/References/<area>`) |
| The bar itself: recipe, macros, suppliers | `product/` |
| Website | `website/` |
| Instagram | `instagram/` |

## Rules (Anton's words win; newest wins)

- [2026-10-15, design kickoff] Nature and outdoor inspired, clean and premium. Mountains on the packaging. ("very nature- and outdoor-inspired, but maybe with a clean, premium look… I see mountains on the packaging.")
- [2026-10-15, design tools] Anton designs in Figma. The Figma file's local variables (collections Color, Spacing, Radius) and text styles (Display/display, Display/headline, Display/label, Text/title, Text/body, Data/data) use the same names as `design/tokens.json`. When he changes a colour or font in Figma, read it (`get_variable_defs`, `get_screenshot`) and update the design system and `design/` to match; when the design system changes, update Figma.
- Figma is on the free Starter plan: max 3 pages per file and 1 mode per variable collection. So Figma holds the light theme only (the dark values live in the design system), and new work goes in sections on the Designs page, not new pages.
- Figma scripting: when binding a colour variable to a paint, pass the token's real colour as the paint's base colour, not black (a bound paint whose base is black rendered black on an instance).
- The design system artifact is the live source; after changing it, copy `tokens.json` and the README back to `design/` (README as `brand-book.md`) and commit.
- Every new design (pack, page, post) is built from the design system's tokens and rules. If a design needs something the system lacks, add it to the system first.

## Feeding references

1. Anton drops screenshots into Dropbox `/[08] GoatBar/References/` in the right folder: Packaging, Website, Instagram, The Bar, Type and Colour, Photography and Mood. Links can be pasted in chat.
2. Claude looks at each new file (Dropbox connector `download_link`), adds one entry to `references/catalog.json`: `{"file", "dropbox_id", "area", "source", "what_we_like", "take": [...], "avoid": [...], "added"}`. `take` and `avoid` are concrete (colour, type, layout, material, photo style).
3. When several references agree on something, it becomes a rule in the design system and a line under Rules above. Anton's notes on a reference ("love the paper texture") count as rules.
