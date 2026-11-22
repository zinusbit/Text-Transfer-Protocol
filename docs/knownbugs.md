## Known Bugs / Quirks

| Issue | Location | Status |
|-------|----------|--------|
| Server sends `ACK` twice (line 25 and line 29) | `server.py` | fixed |
| Client compares `data == b'\x01'` but server sends `b'1'` — byte vs string mismatch | `client.py:45`, `server.py:7` | fixed |
| `msglen = len(message)` counts characters, not UTF-8 bytes — multi-byte chars break the length field | `client.py:18` | fixed |
| `checknochars()` and `checkmaxchars()` return `0` instead of the message | `errcheck.py:18,24` | fixed |
| Server accepts one connection then exits | `server.py` | fixed |
| No TCP framing/length-prefix — `recv(1024)` can split or merge frames | `client.py`, `server.py` | waitng to be fixed
| Spelling: `reciever.py` → should be `receiver.py` | filename | too lazy to fix (not fixed) |

---