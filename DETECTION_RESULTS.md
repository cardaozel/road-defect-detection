# Detection Visualization Results

## Summary

The trained YOLOv8-nano model has been evaluated and detection visualizations have been generated.

## Model Performance

Based on the evaluation report (`results/yolov8n_rdd2022/evaluation/evaluation_summary.txt`):

### Overall Metrics:
- **mAP@0.5**: 29.4% (Mean Average Precision at IoU=0.5)
- **mAP@0.5:0.95**: 11.87% (COCO-style mAP)
- **Precision**: 49.18% (of predictions, 49% are correct)
- **Recall**: 30.34% (finds 30% of actual defects)
- **F1 Score**: 37.53%
- **Balanced Accuracy**: 39.76%

### Model Statistics:
- **Model Size**: 5.93 MB
- **Parameters**: 3.01M

## Detection Visualizations

Detection examples with confidence percentages are saved in:
```
runs/detections/
```

### How to Generate More Examples

Run the visualization script:
```bash
python scripts/visualize_detections.py \
    --weights results/yolov8n_rdd2022/weights/best.pt \
    --source data/yolo/images/val \
    --num-images 10 \
    --conf 0.25 \
    --output-dir runs/detections
```

### Options:
- `--weights`: Path to trained model weights (default: `results/yolov8n_rdd2022/weights/best.pt`)
- `--source`: Image source (directory, single image, or glob pattern)
- `--num-images`: Number of images to process (default: 5)
- `--conf`: Confidence threshold (default: 0.25)
- `--output-dir`: Directory to save annotated images (default: `runs/detections`)

### Output Format

Each annotated image includes:
1. **Bounding boxes** drawn around detected defects
2. **Labels** on each box showing class name and confidence percentage
3. **Confidence summary** displayed as text below the image listing all detections with their percentages

Example output text below image:
```
Detections:
  D00: 39.6%
  D00: 28.0%
```

## Class Definitions

The model detects 6 types of road defects:
- **D00**: Longitudinal crack (crack parallel to road direction)
- **D01**: Transverse crack (crack perpendicular to road direction)
- **D10**: Alligator crack (network of interconnected cracks)
- **D11**: Pothole
- **D20**: Marking blur (faded road markings)
- **D40**: Road repair patches

## Notes

The model performance indicates it's still learning (only trained to epoch 78/100 before being killed). To improve results:
1. Resume training to complete all 100 epochs
2. Consider fine-tuning hyperparameters
3. The model shows decent precision (49%) but lower recall (30%), suggesting it's conservative in making predictions
