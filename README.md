# last_one

# Build Environment

This section provides a detailed overview of the necessary hardware and software environment required for the project.

## Hardware Requirements

- **NVIDIA GPU** 
  - Memory ≥ 2GB
  - NVIDIA Compute capability ≥ 3.0
- **Compatible with:**
  - NVIDIA Jetson Nano
  - NVIDIA Jetson TX2
  - NVIDIA Jetson Xavier
- **CPU**
  - Dual-core processor ≥ 2.4GHz
  - Minimum 4GB RAM

## Software Requirements

This section will provide an explanation on how to configure the ZED2 camera and set up a software environment for skeleton-based action recognition. Before proceeding with the actual environment configuration, ensure that an appropriate version of CUDA is installed.

### Setting Up ZED2 Camera

Follow the steps below to install and configure the ZED2 Camera:

1. [Download the corresponding version of the ZED SDK](https://www.stereolabs.com/developers/release/). [^1^]
2. Install `zedpy`. Note: Directly installing this Python library through pip will only allow you to install `pyzed-1.3.0`, which is not compatible with ZED SDK 4.0. You need to locate the installation files in the default installation path.

### Setting Up SKELETON-BASED ACTION RECOGNITION

The guidance is based on the official documentation. [^2^]

1. Install Python (version should be greater than 3.7).
2. [Install PyTorch on the GPU platform](https://pytorch.org/get-started/locally/). The corresponding version can be found in the official PyTorch documentation. [^3^]
3. Use `mim` to install MMEngine, MMCV, MMDetection, and MMPose:
   ```bash
   pip install -U openmim
   mim install mmengine
   mim install mmcv
   mim install mmdet
   mim install mmpose
   ```
4. [Install `mmaction2` from the source](https://github.com/openmmlab/mmaction2.git). [^4^]

---

[^1^]: [Stereolabs](https://www.stereolabs.com/developers/release/)
[^2^]: [MMAction2 Documentation](#)
[^3^]: [PyTorch Documentation](https://pytorch.org/get-started/locally/)
[^4^]: [MMAction2 GitHub Repository](https://github.com/openmmlab/mmaction2.git)

---

Note: The footnotes format used above (`[^1^]`) is one of the common ways to represent footnotes in Markdown, but GitHub does not natively support footnotes. The links are directly accessible, but if you want the exact footnote behavior, you might need to use a different platform or tool that supports Markdown footnotes.
