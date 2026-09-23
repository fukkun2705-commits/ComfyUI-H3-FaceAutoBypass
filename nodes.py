
from __future__ import annotations
import os, numpy as np, torch
import folder_paths
from ultralytics import YOLO

_MODEL_CACHE = {}

def _candidate_roots():
    roots = [os.path.join(folder_paths.models_dir, "ultralytics")]
    try:
        for key, value in folder_paths.folder_names_and_paths.items():
            if "ultralytics" not in str(key).lower():
                continue
            paths = value[0] if isinstance(value, tuple) and value else value
            if isinstance(paths, (list, tuple, set)):
                roots.extend(str(p) for p in paths)
            elif paths:
                roots.append(str(paths))
    except Exception:
        pass
    out, seen = [], set()
    for r in roots:
        if r:
            r = os.path.normpath(r)
            if r not in seen:
                seen.add(r); out.append(r)
    return out

def _find_model(name):
    wanted = os.path.normpath(str(name)).lower()
    base = os.path.basename(wanted)
    for root in _candidate_roots():
        if not os.path.isdir(root):
            continue
        direct = os.path.join(root, os.path.normpath(str(name)))
        if os.path.isfile(direct):
            return direct
        for dirpath, _, files in os.walk(root):
            for fn in files:
                if fn.lower() == base:
                    return os.path.join(dirpath, fn)
    raise FileNotFoundError(f"Could not find Ultralytics model '{name}'")

def _load_yolo(path):
    if path not in _MODEL_CACHE:
        _MODEL_CACHE[path] = YOLO(path)
    return _MODEL_CACHE[path]

def _to_bgr_u8(frame):
    arr = np.clip(frame.detach().cpu().numpy() * 255.0, 0, 255).astype(np.uint8)
    return arr[..., ::-1].copy()

class H3FacePresenceGate:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":{
            "images":("IMAGE",),
            "face_detector":("STRING",{"default":"face_yolov8m.pt"}),
            "person_detector":("STRING",{"default":r"segm\person_yolov8m-seg.pt"}),
            "face_confidence":("FLOAT",{"default":0.20,"min":0.01,"max":1.0,"step":0.01}),
            "person_confidence":("FLOAT",{"default":0.20,"min":0.01,"max":1.0,"step":0.01}),
            "scan_stride":("INT",{"default":1,"min":1,"max":12,"step":1}),
        }}
    RETURN_TYPES=("BOOLEAN","STRING")
    RETURN_NAMES=("use_refine","report")
    FUNCTION="check"
    CATEGORY="MiniMax H3/Face Refine"

    def check(self, images, face_detector, person_detector, face_confidence=0.20, person_confidence=0.20, scan_stride=1):
        n=int(images.shape[0])
        if n<=0:
            return (False,"AutoBypass: empty batch -> original frames.")
        idx=list(range(0,n,max(1,int(scan_stride))))
        if n-1 not in idx: idx.append(n-1)

        # SAFE RULE: FaceRefine only starts if at least one actual face exists.
        face_model=_load_yolo(_find_model(face_detector))
        for i in idx:
            r=face_model.predict(_to_bgr_u8(images[i]), conf=float(face_confidence), verbose=False)[0]
            if getattr(r,"boxes",None) is not None and len(r.boxes):
                return (True, f"AutoBypass: face detected at frame {i}/{n-1} -> FaceRefine enabled.")

        # Person detection is informational only. Person-only is NOT enough to safely start H3FaceTrackCrop.
        person_found=False
        try:
            person_model=_load_yolo(_find_model(person_detector))
            for i in idx:
                r=person_model.predict(_to_bgr_u8(images[i]), conf=float(person_confidence), verbose=False)[0]
                if getattr(r,"boxes",None) is not None and len(r.boxes):
                    person_found=True; break
        except Exception:
            pass

        if person_found:
            return (False, "AutoBypass: person detected but zero face detections in the whole clip -> FaceRefine skipped; original frames preserved.")
        return (False, "AutoBypass: zero face detections in the whole clip -> FaceRefine skipped; original frames preserved.")

class H3LazyImageSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":{
            "use_refine":("BOOLEAN",),
            "original":("IMAGE",{"lazy":True}),
            "refined":("IMAGE",{"lazy":True}),
        }}
    RETURN_TYPES=("IMAGE",)
    RETURN_NAMES=("images",)
    FUNCTION="select"
    CATEGORY="MiniMax H3/Face Refine"

    def check_lazy_status(self, use_refine, original=None, refined=None):
        needed="refined" if bool(use_refine) else "original"
        val=refined if bool(use_refine) else original
        return [needed] if val is None else []

    def select(self, use_refine, original=None, refined=None):
        return (refined if bool(use_refine) else original,)

NODE_CLASS_MAPPINGS={
    "H3FacePresenceGate":H3FacePresenceGate,
    "H3LazyImageSwitch":H3LazyImageSwitch,
}
NODE_DISPLAY_NAME_MAPPINGS={
    "H3FacePresenceGate":"H3 Face Presence Gate (Auto Bypass)",
    "H3LazyImageSwitch":"H3 FaceRefine Auto Bypass Switch",
}
