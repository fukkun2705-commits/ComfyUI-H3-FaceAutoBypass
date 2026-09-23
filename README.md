# ComfyUI-H3-FaceAutoBypass v2

- At least one face detected in the clip -> FaceRefine runs.
- Face detection drops out on some frames -> H3FaceTrackCrop may use person fallback.
- ZERO face detections in the entire clip -> FaceRefine is skipped and original frames are preserved.

Important: person detection alone is not enough to start FaceRefine safely, because H3FaceTrackCrop still needs at least one actual face detection somewhere in the clip.
## Installation

Open a terminal in your ComfyUI `custom_nodes` directory:

```bash
git clone https://github.com/fukkun2705-commits/ComfyUI-H3-FaceAutoBypass.git
