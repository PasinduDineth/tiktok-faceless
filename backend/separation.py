import torch
import cv2
import numpy as np

# Load better MiDaS model (more accurate than small)
print("Loading MiDaS model...")
midas = torch.hub.load("intel-isl/MiDaS", "MiDaS")
midas.eval()

# Load transforms
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.default_transform

# Load image
img = cv2.imread("scene.png")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Apply transform
input_tensor = transform(img_rgb)

# Ensure correct shape [1, 3, H, W]
if input_tensor.ndim == 3:
    input_batch = input_tensor.unsqueeze(0)
elif input_tensor.ndim == 4 and input_tensor.shape[1] == 1:
    input_batch = input_tensor.squeeze(1)
else:
    input_batch = input_tensor

print("Final input shape:", input_batch.shape)

# Run model
with torch.no_grad():
    prediction = midas(input_batch)

# Resize prediction to original image size
prediction = torch.nn.functional.interpolate(
    prediction.unsqueeze(1),
    size=img_rgb.shape[:2],
    mode="bicubic",
    align_corners=False,
).squeeze()

depth = prediction.cpu().numpy()

# Apply smoothing to reduce noise
depth_smooth = cv2.GaussianBlur(depth, (5, 5), 1.0)

# Normalize depth to 0–255
depth_norm = cv2.normalize(depth_smooth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
cv2.imwrite("depth_map.png", depth_norm)

# Adaptive thresholding based on depth distribution
p25, p75 = np.percentile(depth_norm, [25, 75])
print(f"Adaptive thresholds - Foreground: >{p75:.1f}, Background: <{p25:.1f}")

# Split into 3 layers with adaptive thresholds
h, w = depth_norm.shape
foreground_mask = depth_norm > p75
midground_mask = (depth_norm >= p25) & (depth_norm <= p75)
background_mask = depth_norm < p25

# Clean up masks with morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
foreground_mask = cv2.morphologyEx(foreground_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel).astype(bool)
midground_mask = cv2.morphologyEx(midground_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel).astype(bool)
background_mask = cv2.morphologyEx(background_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel).astype(bool)

def save_layer(mask, name):
    # Create RGBA layer
    layer = np.zeros((h, w, 4), dtype=np.uint8)  # RGBA
    
    # Set RGB channels where mask is True
    layer[mask, :3] = img[mask]
    
    # Set alpha channel to 255 (opaque) where mask is True
    layer[mask, 3] = 255
    
    cv2.imwrite(name, layer)

save_layer(foreground_mask, "foreground.png")
save_layer(midground_mask, "midground.png")
save_layer(background_mask, "background.png")

print("✅ Done! Saved depth_map.png, foreground.png, midground.png, background.png")
