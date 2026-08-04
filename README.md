# DeskRec — Website

Marketing site for **DeskRec**, the native Windows screen recorder (a Screen
Studio alternative) built in [../screen-studio](../screen-studio).

A light, clean, product-focused static site inspired by Screen Studio's
website. Pure HTML + CSS + a little vanilla JS — no build step. Open
`index.html` in a browser (or serve the folder with any static server).

## Pages

| Page | Purpose |
|------|---------|
| `index.html` | Landing page — hero, stats, features, how-it-works, showcase, pricing, FAQ, CTA |
| `features.html` | Detailed feature breakdown |
| `download.html` | Get started / install steps |
| `faq.html` | Frequently asked questions |
| `changelog.html` | Release notes (seeded from the app's git history) |

## Structure

```
deskrec-website/
  index.html
  features.html
  download.html
  faq.html
  changelog.html
  css/styles.css    # all styling (brand in :root)
  js/main.js        # mobile menu, FAQ accordion, scroll-reveal
```

## Brand / editing

- Colors are defined once in `css/styles.css` under `:root` (accent is the
  app's purple `#6c5ce7`). Change there to re-theme the whole site.
- Shared components (nav, footer, buttons, cards) are the same block duplicated
  across pages — edit all copies, or extract partials if you later add a build.

## TODO before going live

- **Pricing** — `index.html` shows placeholder $49 one-time / $149 team pricing.
  Update to your real numbers or license model.
- **Screenshots / video** — the hero window and `.feature-media` /
  `.shot .media` blocks are pure-CSS placeholders. Drop in real product screenshots
  (or an embedded demo video) for a more compelling hero.
- **Contact / email** — swap `hello@deskrec.app` for your real address.
- **Download link** — the primary Download button points at the latest GitHub
  Release of `Michael5565/deskrec` (a working release is published). When you
  publish a new version, the URL stays valid because it resolves
  `releases/latest`.
