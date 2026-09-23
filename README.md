# ComfyUI-H3-FaceAutoBypass v2

`ComfyUI-H3-FaceAutoBypass` is a small custom node extension for ComfyUI that automatically decides whether MiniMax H3 FaceRefine should run for a video clip.

It is designed to work together with `ComfyUI-H3-FaceRefine` and helps avoid unnecessary FaceRefine processing when no face is detected in the generated clip.

## Main Features

- Detects whether at least one face exists in the clip.
- Automatically enables FaceRefine when a face is detected.
- Automatically bypasses FaceRefine when no face is detected.
- Preserves the original video frames when FaceRefine is skipped.
- Reduces unnecessary FaceRefine processing on clips without visible faces.
- Designed for MiniMax H3 video workflows using FaceRefine.

## Included Nodes

- `H3FacePresenceGate`
- `H3LazyImageSwitch`

### H3FacePresenceGate

Checks the generated video frames and determines whether FaceRefine should be enabled.

### H3LazyImageSwitch

Switches automatically between:

```text
Face detected
→ FaceRefine output
```

and

```text
No face detected
→ Original frames
```

## v2 Behavior

- At least one face detected in the clip -> FaceRefine runs.
- Face detection drops out on some frames -> H3FaceTrackCrop may use person fallback.
- ZERO face detections in the entire clip -> FaceRefine is skipped and original frames are preserved.

Important: person detection alone is not enough to start FaceRefine safely, because `H3FaceTrackCrop` still needs at least one actual face detection somewhere in the clip.

## Installation

Open a terminal in your ComfyUI `custom_nodes` directory:

```bash
git clone https://github.com/fukkun2705-commits/ComfyUI-H3-FaceAutoBypass.git
```

Then restart ComfyUI.

## Related Project

This custom node is intended to be used together with:

```text
ComfyUI-H3-FaceRefine
```

Repository:

```text
https://github.com/Carasibana/ComfyUI-H3-FaceRefine
```
