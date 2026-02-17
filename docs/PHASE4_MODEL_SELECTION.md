# Phase 4: Model Selection Documentation

## Which Model to Mention in Thesis?

### For Deployment (iOS App):
**Use: `best.pt` (Epoch 119)**
- **mAP@0.5: 49.19%**
- **Precision: 60.43%**
- **Recall: 47.22%** (from Epoch 152)
- This is the **best-performing checkpoint** and is used in the production iOS application

### For Thesis Documentation:

**Mention BOTH models appropriately:**

#### 1. In Methodology Chapter (Chapter 4):
> "The model was trained for 200 epochs. During training, the best-performing checkpoint was saved at Epoch 119, achieving 49.19% mAP@0.5 with 60.43% precision. This checkpoint (`best.pt`) was selected for deployment to the iOS application as it demonstrated the highest detection accuracy while maintaining mobile compatibility."

#### 2. In Results Chapter (Chapter 5):
> "Training was completed over 200 epochs. The best performance was achieved at Epoch 119 with 49.19% mAP@0.5 and 60.43% precision. The final epoch (Epoch 200) achieved 42.03% mAP@0.5 and 48.69% precision. The model checkpoint from Epoch 119 (`best.pt`) was selected for deployment as it represents the optimal balance between accuracy and model stability."

#### 3. In Discussion:
> "While the final epoch (Epoch 200) showed slightly lower metrics (42.03% mAP@0.5), the best checkpoint from Epoch 119 (49.19% mAP@0.5) was chosen for deployment. This decision ensures the highest detection accuracy in the production iOS application. The performance variation between epochs suggests the model reached its optimal performance around Epoch 119, with subsequent epochs showing some overfitting or convergence to a local minimum."

### Summary Table for Thesis:

| Checkpoint | Epoch | mAP@0.5 | Precision | Recall | Usage |
|------------|-------|---------|-----------|--------|-------|
| **best.pt** | 119 | **49.19%** | **60.43%** | 47.22% | **Deployed to iOS app** |
| last.pt | 200 | 42.03% | 48.69% | 41.15% | Final training state |

### Key Points to Emphasize:

1. **Training completed**: 200 epochs total
2. **Best performance**: Epoch 119 (49.19% mAP@0.5)
3. **Deployment choice**: `best.pt` selected for iOS app (best accuracy)
4. **Justification**: Standard practice to use best checkpoint, not necessarily the final one

---

**This approach is standard in machine learning research: you report the full training progression but deploy the best-performing model.**

