# Agnes Video API - Curl Examples

All examples use `https://apihub.agnes-ai.com/v1/videos` with `Authorization: Bearer $AGNES_API_KEY`.

## Text-to-video (2.5 Flash, default)

```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-2.5-flash",
    "prompt": "A cinematic shot of a cat walking on the beach at sunset, soft ocean waves, warm golden lighting, realistic motion",
    "size": "720P",
    "aspect_ratio": "16:9",
    "mode": "ti2vid"
  }'
```

## Image-to-video

```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-2.5-flash",
    "prompt": "The woman slowly turns around and looks back at the camera, natural facial expression, cinematic camera movement",
    "image": "https://example.com/image.png",
    "size": "720P",
    "aspect_ratio": "16:9",
    "mode": "ti2vid"
  }'
```

## Keyframe animation

```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-2.5-flash",
    "prompt": "Generate a smooth cinematic transition between the keyframes, maintaining visual consistency and natural camera movement",
    "extra_body": {
      "image": [
        "https://example.com/keyframe1.png",
        "https://example.com/keyframe2.png"
      ],
      "mode": "keyframes"
    },
    "num_frames": 121,
    "frame_rate": 24
  }'
```

## Poll for result

```bash
curl -X GET "https://apihub.agnes-ai.com/agnesapi?video_id=<VIDEO_ID>" \
  -H "Authorization: Bearer $AGNES_API_KEY"
```
