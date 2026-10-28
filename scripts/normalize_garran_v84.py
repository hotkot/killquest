"""Insert two generated rear-facing poses in the user's exact nine-pose order.

Existing frames are copied byte-for-byte. Only the two new sprites are scaled
and registered, using one shared scale and the existing planted-foot baseline.
"""
from pathlib import Path
import json, shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, find_objects, binary_opening, binary_dilation

root = Path(__file__).resolve().parents[1]
src = root / 'source-art/garran-v84'
out = root / 'dist/assets/characters'
a = np.array(Image.open(src / 'back-transitions.png').convert('RGBA'))
lab, n = label(binary_opening(a[:, :, 3] > 32))
areas = np.bincount(lab.ravel())
slices = find_objects(lab)
ids = sorted([i for i in range(1, n + 1) if areas[i] > 1000],
             key=lambda i: slices[i - 1][1].start)
assert len(ids) == 2, ('expected exactly two complete poses', len(ids))
cells, heights = [], []
for k in ids:
    sy, sx = slices[k - 1]
    l, r = max(0, sx.start - 4), min(a.shape[1], sx.stop + 4)
    t, b = max(0, sy.start - 4), min(a.shape[0], sy.stop + 4)
    v = a[t:b, l:r].copy()
    v[:, :, 3] = np.where(binary_dilation(lab[t:b, l:r] == k, iterations=3), v[:, :, 3], 0)
    ys = np.where(v[:, :, 3] > 32)[0]
    heights.append(int(ys.max() - ys.min() + 1))
    cells.append(Image.fromarray(v))
# Match the existing two rear-left poses' mean plume-to-sole silhouette height.
target_heights = []
for i in [7, 8]:
    v = np.array(Image.open(src / f'reference-knight-cross-{i:02}.png'))
    ys = np.where(v[:, :, 3] > 32)[0]
    target_heights.append(int(ys.max() - ys.min() + 1))
scale = float(np.mean(target_heights) / np.mean(heights))
report = {'source_order': ['R3C2', 'R3C3', 'new-back', 'new-back-right', 'R2C3', 'R2C2', 'R2C1', 'R1C3', 'R1C2'],
          'shared_scale': scale, 'source_heights': heights, 'target_heights': target_heights, 'new_frames': []}
for j, cell in enumerate(cells, 2):
    cell = cell.resize((round(cell.width * scale), round(cell.height * scale)), Image.Resampling.LANCZOS)
    alpha = np.array(cell)[:, :, 3]
    widths = (alpha > 32).sum(axis=1)
    foot_base = int(np.where(widths >= max(12, round(cell.width * .04)))[0].max())
    y = 408 - foot_base
    gy = np.arange(cell.height)[:, None]
    xs = np.where((alpha > 100) & (gy > foot_base - 22) & (gy <= foot_base))[1]
    anchor = (np.percentile(xs, 10) + np.percentile(xs, 90)) / 2
    x = round(320 - anchor)
    assert x >= 4 and x + cell.width <= 636 and y >= 4 and y + cell.height <= 440
    canvas = Image.new('RGBA', (640, 448))
    canvas.alpha_composite(cell, (x, y))
    canvas.save(out / f'knight-cross-{j:02}.png')
    report['new_frames'].append({'frame': j, 'translation': [x, y], 'ground': 408, 'stance_center': 320})
for dst, original in [(0, 7), (1, 8), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1)]:
    shutil.copyfile(src / f'reference-knight-cross-{original:02}.png', out / f'knight-cross-{dst:02}.png')
for i in range(9, 12):
    (out / f'knight-cross-{i:02}.png').unlink(missing_ok=True)
(src / 'registration.json').write_text(json.dumps(report, indent=2) + '\n')
sheet = Image.new('RGB', (960, 3 * 248), (28, 31, 35))
d = ImageDraw.Draw(sheet)
for i, name in enumerate(report['source_order']):
    im = Image.open(out / f'knight-cross-{i:02}.png').resize((320, 224), Image.Resampling.LANCZOS)
    x, y = i % 3 * 320, i // 3 * 248
    sheet.paste(im, (x, y), im)
    d.text((x + 12, y + 229), f'{i + 1}: {name}', fill='white')
sheet.save(src / 'second-strike-preview.jpg', quality=94)
frames, durations = [], []
for clip, count, times in [
    ('down', 8, [50, 40, 50, 40, 50, 40, 50, 20]),
    ('cross', 9, [60, 60, 60, 60, 50, 50, 50, 40, 30]),
    ('thrust', 12, [50, 40, 50] * 4),
]:
    for i, duration in enumerate(times):
        im = Image.open(out / f'knight-{clip}-{i:02}.png').resize((480, 336), Image.Resampling.LANCZOS)
        bg = Image.new('RGB', im.size, (28, 31, 35))
        bg.paste(im, (0, 0), im)
        frames.append(bg)
        durations.append(duration)
durations[-1] += 500
frames[0].save(src / 'combo-preview.gif', save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)
print('Assembled exact nine-frame second strike; first slash and stab unchanged.')
