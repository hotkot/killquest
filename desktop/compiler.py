"""KillQuest Windows x64 builder: standard-library CLI and Tk desktop UI."""
from pathlib import Path
import argparse
import hashlib
import json
import queue
import re
import shutil
import struct
import subprocess
import sys
import threading
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = ROOT / 'desktop'
OUTPUT = DESKTOP / 'output'
CACHE = DESKTOP / '.cache'
BUILD = OUTPUT / 'KillQuest-Windows-x64'
ARCHIVE = OUTPUT / 'KillQuest-Windows-x64.zip'
ELECTRON = '45.2.1'
CHECKS = ('four-player-selection', 'carion-campaign-v167', 'city-route-v167',
          'city-ambient-v176', 'object-shadow-scene-v179', 'boot-flow', 'start-screen')


def stream_digest(stream):
    checksum = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        checksum.update(chunk)
    return checksum.hexdigest()


def digest(path):
    with path.open('rb') as stream:
        return stream_digest(stream)


def remove_if_present(path):
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def is_within(path, directory):
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def sources():
    files = {f'game/{p.relative_to(ROOT / "dist").as_posix()}': p
             for p in sorted((ROOT / 'dist').rglob('*')) if p.is_file()}
    for name in ('main.cjs', 'asset-path.cjs', 'package.json'):
        files[name] = DESKTOP / name
    files['icon.png'] = ROOT / 'dist/assets/ui/life-head.png'
    return files


def validate_source():
    for name in ('index.html', 'game.js', 'assets/phaser.min.js'):
        if not (ROOT / 'dist' / name).is_file():
            raise RuntimeError(f'Missing game source: dist/{name}')
    inventory = (ROOT / 'dist/loading-assets.js').read_text(encoding='utf-8')
    urls = re.findall(r'"(assets/[^"\n]+)"', inventory)
    if not urls:
        raise RuntimeError('Empty boot asset inventory')
    missing = [u for u in urls if not (ROOT / 'dist' / u.split('?')[0]).is_file()]
    if missing:
        raise RuntimeError('Missing game assets: ' + ', '.join(missing))


def download(url, target, log):
    log(f'Downloading {url}')
    partial = target.with_suffix(target.suffix + '.part')
    try:
        with urllib.request.urlopen(url, timeout=120) as response, partial.open('wb') as out:
            shutil.copyfileobj(response, out)
        partial.replace(target)
    finally:
        remove_if_present(partial)


def runtime(log):
    CACHE.mkdir(parents=True, exist_ok=True)
    filename = f'electron-v{ELECTRON}-win32-x64.zip'
    base = f'https://github.com/electron/electron/releases/download/v{ELECTRON}/'
    sums = CACHE / f'SHASUMS256-v{ELECTRON}.txt'
    if not sums.exists():
        download(base + 'SHASUMS256.txt', sums, log)
    entries = [line.split() for line in sums.read_text().splitlines()]
    matches = [parts[0] for parts in entries if len(parts) == 2 and parts[1].lstrip('*') == filename]
    if len(matches) != 1 or not re.fullmatch('[0-9a-f]{64}', matches[0]):
        raise RuntimeError('Official Electron checksum entry missing or invalid; clear desktop/.cache and retry')
    archive = CACHE / filename
    if not archive.exists():
        download(base + filename, archive, log)
    if digest(archive) != matches[0]:
        archive.unlink()
        raise RuntimeError('Electron checksum mismatch. Cached archive removed; retry to download again.')
    return archive, matches[0]


def verify_pe(path):
    with path.open('rb') as stream:
        header = stream.read(64)
        if len(header) < 64 or header[:2] != b'MZ':
            raise RuntimeError('Invalid Windows executable')
        stream.seek(struct.unpack_from('<I', header, 0x3c)[0])
        if stream.read(6) != b'PE\0\0\x64\x86':
            raise RuntimeError('Executable is not Windows x64')


def build(log=print):
    validate_source()
    archive, checksum = runtime(log)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    staging = OUTPUT / '.building'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    try:
        with zipfile.ZipFile(archive) as z:
            for member in z.infolist():
                destination = (staging / member.filename).resolve()
                if not is_within(destination, staging.resolve()):
                    raise RuntimeError('Unsafe runtime archive path')
            if z.testzip() is not None:
                raise RuntimeError('Corrupt Electron ZIP')
            z.extractall(staging)
        (staging / 'electron.exe').rename(staging / 'KillQuest.exe')
        verify_pe(staging / 'KillQuest.exe')
        remove_if_present(staging / 'resources/default_app.asar')
        app = staging / 'resources/app'
        log('Copying current game assets…')
        for relative, source in sources().items():
            target = app / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        shutil.copy2(DESKTOP / 'README.txt', staging / 'READ-ME.txt')
        manifest = {p.relative_to(staging).as_posix(): digest(p)
                    for p in sorted(staging.rglob('*')) if p.is_file()}
        info = {'electron_version': ELECTRON, 'platform': 'win32', 'architecture': 'x64',
                'runtime_sha256': checksum, 'files': manifest}
        (staging / 'build-info.json').write_text(json.dumps(info, indent=2) + '\n')
        # Preserve the previous working build until the new one is fully prepared.
        previous = OUTPUT / '.previous'
        if previous.exists():
            shutil.rmtree(previous)
        if BUILD.exists():
            BUILD.rename(previous)
        try:
            staging.rename(BUILD)
        except Exception:
            if previous.exists():
                previous.rename(BUILD)
            raise
        if previous.exists():
            shutil.rmtree(previous)
        remove_if_present(ARCHIVE)
        log(f'Build complete: {BUILD / "KillQuest.exe"}')
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def verify_build():
    if not (BUILD / 'build-info.json').is_file():
        raise RuntimeError('Build first: no completed EXE build exists.')
    info = json.loads((BUILD / 'build-info.json').read_text())
    expected = info['files']
    actual = {p.relative_to(BUILD).as_posix() for p in BUILD.rglob('*')
              if p.is_file() and p.name != 'build-info.json'}
    if actual != set(expected):
        raise RuntimeError('Build file inventory changed. Build again.')
    for relative, checksum in expected.items():
        if digest(BUILD / relative) != checksum:
            raise RuntimeError(f'Build file changed: {relative}. Build again.')
    current = sources()
    bundled = {p[len('resources/app/'):]: checksum for p, checksum in expected.items()
               if p.startswith('resources/app/')}
    if set(current) != set(bundled) or any(digest(p) != bundled[r] for r, p in current.items()):
        raise RuntimeError('Game source changed since Build. Build again before continuing.')
    if digest(DESKTOP / 'README.txt') != expected['READ-ME.txt']:
        raise RuntimeError('Package instructions changed. Build again.')
    verify_pe(BUILD / 'KillQuest.exe')


def command(args, log):
    log('> ' + ' '.join(map(str, args)))
    with subprocess.Popen(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding='utf-8', errors='replace') as process:
        for line in process.stdout:
            log(line.rstrip())
        if process.wait():
            raise RuntimeError(f'Check failed: {args[-1]}')


def test(log=print):
    validate_source()
    verify_build()
    node = shutil.which('node')
    if not node:
        raise RuntimeError('Install Node.js 22 or newer, then reopen this tool.')
    major = int(subprocess.check_output([node, '-p', 'process.versions.node.split(".")[0]'], text=True))
    if major < 22:
        raise RuntimeError('Node.js 22 or newer is required.')
    for script in sorted((ROOT / 'dist').glob('*.js')):
        command([node, '--check', str(script)], log)
    for name in ('main.cjs', 'asset-path.cjs'):
        command([node, '--check', str(DESKTOP / name)], log)
    for check in CHECKS:
        command([node, str(ROOT / f'checks/{check}.cjs')], log)
    command([node, str(ROOT / 'checks/desktop-path.cjs')], log)
    command([sys.executable, str(ROOT / 'checks/desktop_builder.py')], log)
    log('PASS: game regressions, source freshness, all packaged hashes and Windows x64 EXE.')
    log('Windows gameplay, audio and physical controllers still need an interactive playtest.')


def package(log=print):
    verify_build()
    info_bytes = (BUILD / 'build-info.json').read_bytes()
    expected = json.loads(info_bytes)['files']
    partial = ARCHIVE.with_suffix('.zip.part')
    try:
        with zipfile.ZipFile(partial, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for p in sorted(BUILD.rglob('*')):
                if p.is_file():
                    z.write(p, BUILD.name + '/' + p.relative_to(BUILD).as_posix())
        with zipfile.ZipFile(partial) as z:
            if z.testzip() is not None:
                raise RuntimeError('Package ZIP integrity failed')
            for relative, checksum in expected.items():
                with z.open(BUILD.name + '/' + relative) as stream:
                    if stream_digest(stream) != checksum:
                        raise RuntimeError(f'Package content changed during packaging: {relative}')
            if z.read(BUILD.name + '/build-info.json') != info_bytes:
                raise RuntimeError('Build manifest changed during packaging')
        verify_build()
        partial.replace(ARCHIVE)
    finally:
        remove_if_present(partial)
    log(f'Package complete: {ARCHIVE}\nSHA256: {digest(ARCHIVE)}')


def run(log=print):
    if sys.platform != 'win32':
        raise RuntimeError('Run requires Windows. Copy/extract the complete portable folder on Windows.')
    verify_build()
    process = subprocess.Popen([str(BUILD / 'KillQuest.exe')], cwd=BUILD)
    log(f'Game launched (PID {process.pid}). Use F11 for fullscreen; Alt+F4 to exit.')


def deploy(log=print):
    for action in (build, test, package, run):
        action(log)


ACTIONS = {'build': build, 'test': test, 'package': package, 'run': run, 'deploy': deploy}


def gui():
    import tkinter as tk
    from tkinter import ttk
    window = tk.Tk()
    window.title('KillQuest — EXE Builder')
    window.geometry('940x640')
    window.minsize(700, 460)
    background = '#15171c'
    foreground = '#e6e8ee'
    window.configure(background=background)
    if sys.platform == 'win32':
        # Request a dark native title bar on Windows versions that support it.
        try:
            import ctypes
            from ctypes import wintypes
            window.update_idletasks()
            get_parent = ctypes.windll.user32.GetParent
            get_parent.argtypes = [wintypes.HWND]
            get_parent.restype = wintypes.HWND
            hwnd = get_parent(window.winfo_id()) or window.winfo_id()
            enabled = wintypes.BOOL(True)
            set_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            set_attribute.argtypes = [wintypes.HWND, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD]
            for attribute in (20, 19):
                if set_attribute(hwnd, attribute, ctypes.byref(enabled), ctypes.sizeof(enabled)) == 0:
                    break
        except (AttributeError, OSError):
            pass  # Older Windows can still use the dark client area.
    style = ttk.Style(window)
    # Clam respects custom colors on Windows instead of the native light theme.
    style.theme_use('clam')
    style.configure('.', background=background, foreground=foreground)
    style.configure('TFrame', background=background)
    style.configure('TLabel', background=background, foreground=foreground)
    style.configure('TButton', background='#2b303b', foreground=foreground,
                    bordercolor='#454d5e', lightcolor='#2b303b', darkcolor='#2b303b',
                    focuscolor='#97baff', padding=6)
    style.map('TButton', background=[('disabled', '#20242c'), ('pressed', '#3e4e6b'),
                                    ('active', '#364155')],
              foreground=[('disabled', '#858c9b'), ('active', '#ffffff')],
              bordercolor=[('focus', '#97baff')])
    style.configure('Vertical.TScrollbar', background='#353c49', troughcolor='#101216',
                    arrowcolor=foreground, bordercolor=background,
                    lightcolor='#353c49', darkcolor='#353c49')
    style.map('Vertical.TScrollbar', background=[('pressed', '#596b89'), ('active', '#47546a')])
    frame = ttk.Frame(window, padding=18)
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='KillQuest · Windows EXE Builder', font=('Segoe UI', 19, 'bold')).pack(anchor='w')
    ttk.Label(frame, text='Deploy = Build → Test → Package → Run · local Windows x64 portable game').pack(anchor='w', pady=(6, 14))
    toolbar = ttk.Frame(frame)
    toolbar.pack(fill='x')
    status = tk.StringVar(value='Ready — first build downloads the verified Electron runtime.')
    ttk.Label(frame, textvariable=status, wraplength=860).pack(anchor='w', pady=12)
    log_frame = ttk.Frame(frame)
    log_frame.pack(fill='both', expand=True)
    output = tk.Text(log_frame, wrap='word', state='disabled', font=('Consolas', 10),
                     background='#101216', foreground=foreground, insertbackground=foreground,
                     selectbackground='#3b527b', selectforeground='#ffffff',
                     relief='flat', borderwidth=0, highlightthickness=1,
                     highlightbackground='#353c49', highlightcolor='#97baff', padx=12, pady=10)
    scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=output.yview)
    output.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    output.pack(side='left', fill='both', expand=True)
    output.tag_configure('error', foreground='#ff9292')
    ttk.Label(frame, text=f'Output: {OUTPUT}', wraplength=860).pack(anchor='w', pady=(10, 0))
    events = queue.Queue()
    buttons = []
    busy = False

    def start(name):
        nonlocal busy
        busy = True
        for button in buttons:
            button.config(state='disabled')
        status.set(f'{name.title()} in progress…')

        def worker():
            try:
                ACTIONS[name](lambda message: events.put(('log', str(message))))
                events.put(('done', f'{name.title()} complete.'))
            except Exception as error:
                events.put(('error', str(error)))
        threading.Thread(target=worker, daemon=True).start()

    for name in ACTIONS:
        button = ttk.Button(toolbar, text=name.title(), command=lambda n=name: start(n))
        button.pack(side='left', padx=(0, 10), ipadx=12, ipady=7)
        buttons.append(button)

    def poll():
        nonlocal busy
        while not events.empty():
            kind, message = events.get_nowait()
            output.config(state='normal')
            output.insert('end', ('ERROR: ' if kind == 'error' else '') + message + '\n',
                          ('error',) if kind == 'error' else ())
            output.see('end')
            output.config(state='disabled')
            if kind in ('done', 'error'):
                busy = False
                status.set(message)
                for button in buttons:
                    button.config(state='normal')
        window.after(100, poll)

    def close():
        if busy:
            status.set('Wait for the current operation to finish before closing.')
        else:
            window.destroy()
    window.protocol('WM_DELETE_WINDOW', close)
    poll()
    window.mainloop()


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(errors='replace')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', nargs='?', choices=ACTIONS, help='Omit to open the button UI')
    args = parser.parse_args()
    try:
        if args.action:
            ACTIONS[args.action]()
        else:
            gui()
    except Exception as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
