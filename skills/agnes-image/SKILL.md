---
name: agnes-image
description: Use when the user wants to generate, edit, or composite images via the Agnes Image API. Covers text-to-image, image-to-image, multi-image composition, style transfer, background replacement. Requires AGNES_API_KEY.
---

# Agnes Image API

!`[ -z "$AGNES_API_KEY" ] && echo "BLOCKED: AGNES_API_KEY is not set. Export it in your shell before using this skill." || echo "OK: AGNES_API_KEY ready"`

Third-party image generation API (Sapiens AI). Two models:

| Model                   | ID                      | Best for                                                                  |
| ----------------------- | ----------------------- | ------------------------------------------------------------------------- |
| **2.1 Flash** (default) | `agnes-image-2.1-flash` | High-density scenes, complex compositions, detail-rich visuals            |
| **2.0 Flash**           | `agnes-image-2.0-flash` | General-purpose edits, product shots, style transfer. ELO 1,184 (Top 20). |

Use 2.1 unless the user explicitly requests 2.0.

## Parameters

| Parameter                    | Type     | Required     | Notes                                                              |
| ---------------------------- | -------- | ------------ | ------------------------------------------------------------------ |
| `model`                      | string   | Yes          | `agnes-image-2.1-flash` (default) or `agnes-image-2.0-flash`       |
| `prompt`                     | string   | Yes          | Description of target image or edit instruction                    |
| `size`                       | string   | Yes          | e.g. `1024x768`, `1024x1024`, `768x1024`                           |
| `return_base64`              | boolean  | No           | Set true for Base64 output on text-to-image                        |
| `extra_body`                 | object   | No           | Contains `response_format` and `image` for img2img                 |
| `extra_body.response_format` | string   | No           | `url` or `b64_json` - **must** be in `extra_body`, never top-level |
| `extra_body.image`           | string[] | img2img only | Public HTTPS URLs or Data URI Base64                               |

Do not add `tags: ["img2img"]` - it is not part of the schema.

## How it works

**Text-to-image**: Send `model`, `prompt`, `size` (+ optional `extra_body.response_format`).
**Image-to-image**: Add `extra_body.image` array with input images.
**Multi-image composition (2.0 only)**: Multiple entries in `extra_body.image`. 2.1 focuses on single-image editing.

## Prompt construction

- **Text-to-image**: `[Subject] + [Scene] + [Style] + [Lighting] + [Composition] + [Quality]`
- **Editing**: `[Change request] + [Elements to preserve] + [Target style] + [Lighting]` - always state what must stay unchanged.
- **High-density (2.1)**: Describe visual hierarchy explicitly - main subject, background, secondary details, style, composition constraints.

## Response

```json
{
  "created": 1780000000,
  "data": [{ "url": "https://...", "b64_json": null, "revised_prompt": null }]
}
```

Access via `data[0].url` (URL) or `data[0].b64_json` (Base64).

## Gotchas

- `response_format` must be inside `extra_body`, never top-level (causes `400`).
- Input images must be public HTTPS URLs or Data URI Base64.
- Image dimensions must be multiples of 16.
- Timeout: 60-360s. Pricing: $0.003/image standard, currently $0/image promotional.
- 2.1 preserves original composition by default - state explicitly what must change.
- Error codes: `400`, `401`, `402`, `403`, `404`, `422`, `429`, `500`.

For full curl examples, read `references/examples.md`.
