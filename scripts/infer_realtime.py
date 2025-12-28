#!/usr/bin/env python3
"""Run real-time inference using a trained YOLOv8 model."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

import cv2
from ultralytics import YOLO


def configure_logger(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-time detection using YOLOv8.")
    parser.add_argument("--weights", required=True, help="Path to trained weights (best.pt).")
    parser.add_argument("--source", default="0", help="Video source (0 for webcam, path to video, or image glob).")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size.")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold.")
    parser.add_argument("--device", default="cuda", help="Device for inference.")
    parser.add_argument("--save", action="store_true", help="Save annotated video to disk.")
    parser.add_argument("--output", default="runs/inference/output.mp4", help="Path for saved video when --save is set.")
    parser.add_argument("--headless", action="store_true", help="Skip window rendering (useful on servers).")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def resolve_source(source: str) -> str | int:
    if source.isdigit():
        return int(source)
    return source


def create_writer(path: Path, fps: float, width: int, height: int) -> Optional[cv2.VideoWriter]:
    path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, fps if fps > 0 else 30.0, (width, height))
    if not writer.isOpened():
        logging.warning("Failed to open VideoWriter for %s", path)
        return None
    return writer


def main() -> int:
    args = parse_args()
    configure_logger(args.verbose)

    weights = Path(args.weights).expanduser().resolve()
    model = YOLO(str(weights))

    source = resolve_source(args.source)
    logging.info("Running inference on source: %s", source)

    writer: Optional[cv2.VideoWriter] = None
    window_name = "RDD2022 Detection"

    try:
        stream = model.predict(
            source=source,
            stream=True,
            imgsz=args.imgsz,
            conf=args.conf,
            device=args.device,
            verbose=False,
        )

        for result in stream:
            frame = result.plot()
            if writer is None and args.save:
                h, w = frame.shape[:2]
                fps = getattr(result, "speed", {}).get("fps", 30.0)
                writer = create_writer(Path(args.output).expanduser().resolve(), fps, w, h)

            if writer is not None:
                writer.write(frame)

            if not args.headless:
                cv2.imshow(window_name, frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    logging.info("Exit requested (ESC press).")
                    break
    finally:
        if writer is not None:
            writer.release()
        if not args.headless:
            cv2.destroyAllWindows()

    logging.info("Inference session ended.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
