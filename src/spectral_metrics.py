import numpy as np

def rmse(orig: np.ndarray, down: np.ndarray) -> float:
    assert orig.shape == down.shape, "Размеры массивов не совпадают"
    diff = orig - down
    mse = np.mean(diff ** 2)
    return np.sqrt(mse)

def bias(orig: np.ndarray, down: np.ndarray) -> tuple:
    bias_map = down - orig
    mean_bias = np.mean(bias_map, axis=(1, 2))
    return mean_bias, bias_map

def sam(orig: np.ndarray, down: np.ndarray) -> tuple:
    norm_orig = np.linalg.norm(orig, axis=0)
    norm_down = np.linalg.norm(down, axis=0)

    norm_orig = np.where(norm_orig == 0, 1e-10, norm_orig)
    norm_down = np.where(norm_down == 0, 1e-10, norm_down)

    dot = np.sum(orig * down, axis=0)

    cos_theta = dot / (norm_orig * norm_down)
    cos_theta = np.clip(cos_theta, -1, 1)

    sam_rad = np.arccos(cos_theta)
    sam_deg = np.degrees(sam_rad)

    mean_sam = np.mean(sam_deg)
    return mean_sam, sam_deg

def channel_rmse(orig: np.ndarray, down: np.ndarray) -> np.ndarray:
    diff = orig - down
    mse = np.mean(diff ** 2, axis=(1, 2))
    return np.sqrt(mse)

def ergas(orig: np.ndarray, down: np.ndarray, h: float = 1.0, l: float = 1.0) -> float:
    assert orig.shape == down.shape, "Размеры массивов не совпадают"
    bands = orig.shape[0]
    rmse_per_band = np.sqrt(np.mean((orig - down) ** 2, axis=(1, 2)))
    mean_per_band = np.mean(orig, axis=(1, 2))
    ergas_val = 100.0 * (h / l) * np.sqrt(np.sum((rmse_per_band / (mean_per_band + 1e-10)) ** 2) / bands)
    return ergas_val

def channel_correlation(orig: np.ndarray, down: np.ndarray) -> np.ndarray:
    assert orig.shape == down.shape, "Размеры массивов не совпадают"
    r_per_band = np.zeros(orig.shape[0])
    for b in range(orig.shape[0]):
        o = orig[b].ravel()
        d = down[b].ravel()
        mask = np.isfinite(o) & np.isfinite(d)
        if np.sum(mask) < 2:
            r_per_band[b] = np.nan
        else:
            r_per_band[b] = np.corrcoef(o[mask], d[mask])[0, 1]
    return r_per_band

def overall_correlation(orig: np.ndarray, down: np.ndarray) -> float:
    assert orig.shape == down.shape, "Размеры массивов не совпадают"
    o = orig.ravel()
    d = down.ravel()
    mask = np.isfinite(o) & np.isfinite(d)
    if np.sum(mask) < 2:
        return np.nan
    return np.corrcoef(o[mask], d[mask])[0, 1]