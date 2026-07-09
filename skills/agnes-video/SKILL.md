---
name: agnes-video
description: Use when the user wants to generate videos via the Agnes Video API. Covers text-to-video, image-to-video, keyframe animation, motion assets. Requires AGNES_API_KEY.
---

# Agnes Video V2.0

> **Prerequisite:** `AGNES_API_KEY` must be set in your shell environment. If unset, export it before proceeding: `export AGNES_API_KEY="your-key"`.

Third-party asynchronous video generation API (Sapiens AI). Model: `agnes-video-v2.0`.

## Endpoints

| Purpose                  | Method | URL                                                  |
| ------------------------ | ------ | ---------------------------------------------------- |
| Create task              | POST   | `https://apihub.agnes-ai.com/v1/videos`              |
| Get result (recommended) | GET    | `https://apihub.agnes-ai.com/agnesapi?video_id=<ID>` |
| Get result (legacy)      | GET    | `https://apihub.agnes-ai.com/v1/videos/<TASK_ID>`    |

Append `&model_name=agnes-video-v2.0` to the recommended endpoint when using an upstream video ID or explicitly specifying the model.

## Parameters

| Parameter             | Type     | Required | Notes                                         |
| --------------------- | -------- | -------- | --------------------------------------------- |
| `model`               | string   | Yes      | Always `agnes-video-v2.0`                     |
| `prompt`              | string   | Yes      | Text description of video content             |
| `image`               | string   | No       | Public HTTPS URL for image-to-video           |
| `mode`                | string   | No       | `ti2vid` (text/image-to-video) or `keyframes` |
| `height`              | integer  | No       | Default `768`                                 |
| `width`               | integer  | No       | Default `1152`                                |
| `num_frames`          | integer  | No       | `<= 441`, must follow `8n + 1` rule           |
| `frame_rate`          | number   | No       | Range `1-60`                                  |
| `num_inference_steps` | integer  | No       | Inference steps                               |
| `seed`                | integer  | No       | Fixed seed for reproducibility                |
| `negative_prompt`     | string   | No       | Content to avoid                              |
| `extra_body.image`    | string[] | No       | Keyframe input images                         |
| `extra_body.mode`     | string   | No       | `"keyframes"` for keyframe animation          |

## Workflow

1. POST create task -> get `video_id`
2. Poll GET `agnesapi?video_id=<ID>` until `status` is `completed` or `failed`
3. Download from `url` field

Statuses: `queued` -> `in_progress` -> `completed` | `failed`

## Prompt construction

- **Text-to-video**: `[Subject] + [Action] + [Scene] + [Camera Movement] + [Lighting] + [Style]`
- **Image-to-video**: Describe what should move and what should stay stable.
- **Keyframes**: Describe the transition between keyframes, maintaining identity and consistency.

## Response

```json
{
  "video_id": "video_xxx",
  "status": "completed",
  "url": "https://...",
  "seconds": "10.0",
  "size": "1280x768"
}
```

Use `video_id` (not `task_id`) to retrieve results. After normalization, `seconds` and `size` from response are source of truth.

## Gotchas

- Async workflow - always poll until `completed` or `failed`.
- `num_frames` must be `<= 441` and follow `8n + 1` rule.
- `frame_rate` range `1-60`. Higher = smoother but shorter duration.
- Video dimensions must be multiples of 64.
- Input images must be public HTTPS URLs.
- Timeout: tens of seconds to several minutes. Poll every 5-10s.
- Pricing: $0.005/second standard, currently $0/second promotional.
- Error codes: `400`, `401`, `402`, `403`, `404`, `405`, `408`, `409`, `413`, `422`, `429`, `500`, `502`, `503`.

For curl examples, read `references/examples.md`. For duration/resolution tables, read `references/parameters.md`.
