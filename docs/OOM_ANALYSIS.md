# Why Training Was Killed at Epoch 94/100

## Analysis

Based on the system state and training configuration, here are the most likely reasons:

## Root Causes

### 1. **MPS Unified Memory Limits** (Most Likely)
- **MPS (Metal Performance Shaders)** on macOS uses **unified memory** shared between CPU and GPU
- After 94 epochs (~70+ hours), memory fragmentation and accumulation occur
- MPS doesn't always release memory as efficiently as CUDA
- Your system has 16GB RAM total, but MPS memory is part of this pool

### 2. **Memory Accumulation Over Time**
- Dataset caching grows over long training runs
- Gradient accumulation and optimizer states persist
- Validation phase (max_det=150) uses additional memory
- Model checkpoints and logging also consume memory

### 3. **macOS Memory Pressure Management**
- macOS **automatically kills processes** when memory pressure is high
- The "zsh: killed" message indicates the OS killed the process, not a Python error
- This happens when available memory drops too low

### 4. **Validation Phase Memory Spike**
- Validation runs after each epoch and uses more memory
- With max_det=150 and 3579 validation images, this creates spikes
- At epoch 94, accumulated state + validation = higher memory usage

## Current Memory Status
- **Total RAM:** 16.0 GB
- **Used:** 7.2 GB (76.2%)
- **Available:** 3.8 GB
- During training, usage likely spiked above available memory

## Solutions to Prevent Future Kills

### Immediate Fixes:

1. **Add Periodic MPS Cache Clearing**
   ```python
   # Clear cache every N epochs
   if epoch % 10 == 0:
       torch.mps.empty_cache()
   ```

2. **Reduce Validation Frequency**
   ```yaml
   val_period: 5  # Validate every 5 epochs instead of every epoch
   ```

3. **Reduce Validation Memory**
   ```yaml
   max_det: 100  # Further reduce from 150
   val_batch: 1  # Smaller validation batch
   ```

4. **Disable Dataset Caching**
   ```yaml
   cache: false  # Don't cache dataset to disk
   ```

### Long-term Solutions:

1. **Increase System Memory** - More RAM (32GB+) helps significantly
2. **Use CPU Training** - More stable but slower (already optimized for MPS)
3. **Use Cloud Training** - AWS/GCP with GPU instances
4. **Train in Stages** - Train 50 epochs, evaluate, then continue

## Why It Happened at 94/100

- Memory gradually accumulates over epochs
- Epoch 94 was likely when accumulated memory + validation spike exceeded available memory
- macOS killed the process to prevent system crash
- The checkpoint was saved successfully, allowing resume

## Current Status

✅ **Good news:** The checkpoint was saved, so training resumed successfully
✅ **Training is now running** from epoch 94 → 100
✅ **Only 6 epochs remaining** - should complete without issues

## Prevention for Next Training

The training script now includes:
- MPS cache clearing before training
- Automatic resume capability
- Optimized memory settings

Consider adding periodic cache clearing during training for longer runs (200+ epochs).

