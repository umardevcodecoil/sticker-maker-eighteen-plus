# Sticker Packs

Sticker pack catalog for the Sticker Maker Android app. The app reads `packs/index.json` and each pack's `manifest.json` through jsDelivr.

## Layout

```
packs/
  index.json                  # all packs: id, name, category, path, isPremium, version
  <category>/
    <pack-id>/
      manifest.json           # name, author, version, isPremium, sticker list
      tray.png                # 96x96 PNG, tray icon (max 50 KB)
      stickers/
        001.webp ...          # 512x512 WebP, 3 to 30 per pack, max 100 KB each
```

## Rules

- Every pack needs a `version`. Bump it whenever the pack changes so the app refreshes its cache.
- Validate before committing: `python3 scripts/validate.py`
- Use tagged releases for the CDN. Serve files via `cdn.jsdelivr.net/gh/<owner>/<repo>@<tag>/packs/...`, not `main`.
- Do not commit content that breaks GitHub's Acceptable Use Policy. Check the policy before adding any pack.
