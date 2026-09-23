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

### 1. Clone the repository

Open a terminal in your ComfyUI `custom_nodes` directory:

```bash
git clone https://github.com/fukkun2705-commits/ComfyUI-H3-FaceAutoBypass.git
```

---

### 2. Install Python dependencies

This custom node requires the `ultralytics` Python package.

If you are using the Python environment already used by ComfyUI:

```bash
python -m pip install -r ComfyUI-H3-FaceAutoBypass/requirements.txt
```

If your ComfyUI installation uses a dedicated virtual environment, run the command using that environment's Python executable.

Example on Windows:

```bat
<ComfyUI Folder>\venv\Scripts\python.exe -m pip install -r <ComfyUI Folder>\custom_nodes\ComfyUI-H3-FaceAutoBypass\requirements.txt
```

---

### 3. Install detector models

The following detector models are required:

```text
face_yolov8m.pt
person_yolov8m-seg.pt
```

Place them in:

```text
ComfyUI/models/ultralytics/bbox/face_yolov8m.pt
ComfyUI/models/ultralytics/segm/person_yolov8m-seg.pt
```

If you use Stability Matrix with a shared Models folder, the detector models may instead be stored under:

```text
Data/Models/Ultralytics/bbox/face_yolov8m.pt
Data/Models/Ultralytics/segm/person_yolov8m-seg.pt
```

---

### 4. Restart ComfyUI

Restart ComfyUI after installation.

If installation is successful, `ComfyUI-H3-FaceAutoBypass` should load without `IMPORT FAILED` in the startup log.
