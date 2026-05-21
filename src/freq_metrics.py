import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, fftshift

def radial_spectrum(image, pixel_size=10.0, return_freqs=True):
    h, w = image.shape
    f = fft2(image)
    fshift = fftshift(f)
    power = np.abs(fshift) ** 2

    cx, cy = w // 2, h // 2
    y, x = np.ogrid[:h, :w]
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    r = r.astype(int)

    max_radius = min(cx, cy)
    radial_means = []
    for rad in range(1, max_radius):
        mask = (r == rad)
        radial_means.append(np.mean(power[mask]))
    radial_means = np.array(radial_means)

    freqs_pix = np.linspace(0.5 / max_radius, 0.5, len(radial_means))
    if return_freqs:
        freqs_m = freqs_pix / pixel_size
        return freqs_m, radial_means
    else:
        return freqs_pix, radial_means

def plot_radial_spectrum(freqs, power_orig, power_sr, save_path=None, title=None, xlim=None, ylim=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(freqs, power_orig, label='Оригинал S2 (10 м)', linewidth=1.6, color='#2166ac')
    ax.loglog(freqs, power_sr, label='S2DR3 (10 м)', linewidth=1.6, color='#b2182b')
    ax.set_xlabel('Пространственная частота (циклов/м)', fontsize=12)
    ax.set_ylabel('Спектральная плотность мощности', fontsize=12)
    if title:
        ax.set_title(title, fontsize=14)
    else:
        ax.set_title('Радиальный спектр мощности', fontsize=14)
    ax.legend(fontsize=10, frameon=True, edgecolor='none', facecolor='white', loc='best')
    ax.grid(True, which='major', linestyle='-', linewidth=0.4, color='grey', alpha=0.4)
    ax.set_facecolor('#f7f7f7')
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

def plot_radial_spectrum_ratio(freqs, power_orig, power_sr, save_path=None, title=None, xlim=None, ylim=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    ratio = power_sr / (power_orig + 1e-12)
    ax.semilogx(freqs, ratio, linewidth=1.6, color='#4daf4a')
    ax.axhline(y=1, linestyle='--', color='grey', alpha=0.7, linewidth=1.0)
    ax.set_xlabel('Пространственная частота (циклов/м)', fontsize=12)
    ax.set_ylabel('Отношение мощности (SR / Оригинал)', fontsize=12)
    if title:
        ax.set_title(f'{title} — Отношение спектров', fontsize=14)
    else:
        ax.set_title('Отношение радиальных спектров', fontsize=14)
    ax.set_yscale('log')
    ax.grid(True, which='major', linestyle='-', linewidth=0.4, color='grey', alpha=0.4)
    ax.set_facecolor('#f7f7f7')
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(0.2, 5.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

def plot_spectrum_diff(freqs, power_orig, power_sr, save_path=None, xlim=None, ylim=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    diff = np.log10(power_sr + 1e-12) - np.log10(power_orig + 1e-12)
    ax.semilogx(freqs, diff, linewidth=1.6, color='#9970ab')
    ax.axhline(y=0, linestyle='--', color='grey', alpha=0.7, linewidth=1.0)
    ax.set_xlabel('Пространственная частота (циклов/м)', fontsize=12)
    ax.set_ylabel('Разность: log10(Super Resolution) - log10(Оригинал)', fontsize=12)
    ax.set_title('Разность спектров (положительное = SR сильнее)', fontsize=14)
    ax.grid(True, which='major', linestyle='-', linewidth=0.4, color='grey', alpha=0.4)
    ax.set_facecolor('#f7f7f7')
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()