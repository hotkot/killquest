"""Embed the authored witch system into the buildless game bundle."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'dist/game.js';s=p.read_text();start=s.index('// WITCH_SYSTEM_BEGIN');end=s.index('// WITCH_SYSTEM_END')+len('// WITCH_SYSTEM_END')
p.write_text(s[:start]+'// WITCH_SYSTEM_BEGIN\n'+(root/'src/witch.js').read_text()+'\n// WITCH_SYSTEM_END'+s[end:])
