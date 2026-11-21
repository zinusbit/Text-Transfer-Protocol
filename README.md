# TTP0 — Text Transfer Protocol v0

*A tiny, teaching-grade protocol for sending text with a CRC-16 checksum. Built for learning, not production.*

---

## TL;DR

TTP0 wraps a text message in a binary frame and sends it over a raw TCP socket:

```
TTP0 + length + Type + your-text + CRC16
```

**Client:** `python src/base-impl/client.py`  
**Server:** `python src/base-impl/server.py`

Run the server first, then the client. Type a message, hit enter, the server parses it, verifies the CRC, and replies with `ACK` (`b'1'`) or `NACK` (`b'2'`).

---

## Why This Exists

Someone wanted to understand how real protocols work under the hood. So they built the simplest possible thing that still has:

- **A magic number** — `0x54 0x54 0x50 0x30` ("TTP0") so receivers know this is TTP0, not JSON or protobuf
- **A length field** — 1 byte so you know when the message ends (max 255 bytes)
- **A message type byte** — so you can distinguish commands from data
- **A checksum (CRC-16/IBM)** — so you can detect corruption

That's it. No headers, no handshakes, no retries. Just framing over TCP.

---

## The Frame (On the Wire)

```
┌─────────────┬───────┬──────────┬────────────┬──────────┐
│  "TTP0"     │ len   │  TYPE    │  payload   │  CRC16   │
│  (4 bytes)  │(1 B)  │  (1 B)   │  (N bytes) │ (2 bytes)│
└─────────────┴───────┴──────────┴────────────┴──────────┘
```

| Bytes | Meaning |
|-------|---------|
| `54 54 50 30` | ASCII `"TTP0"` — protocol ID |
| `0C` | Length of payload in bytes (big-endian, max 255) |
| `04` | Message type byte |
| `48 65 6C 6C 6F...` | Your UTF-8 text payload |
| `1A 2B` | CRC-16 (big-endian: high byte first, then low byte) |

**Example:** `"Hi"` (type `0x04`) → `54 54 50 30 02 04 48 69 <CRC_hi> <CRC_lo>`

---

## Project Structure

```
assembly/
├── LICENSE                       # GNU GPL v3
├── README.md                     # This file
└── src/
    └── base-impl/
        ├── transmitter.py        # CRC16 class + frame builders
        ├── reciever.py           # CRC16 class + parser + CRC checker
        ├── errcheck.py           # NoChars / MacChars exceptions + checkbuffer
        ├── client.py             # TCP client: builds frame, sends over socket
        └── server.py             # TCP server: receives frame, parses, CRC checks, ACK/NACK
```

---

## Components

### `src/base-impl/transmitter.py`

| Name | Purpose |
|------|---------|
| `CRC16` | CRC-16/IBM with 256-entry lookup table |
| `framebuildernocrc(PRTV, MSGLint, TYPE, MSG)` | Builds `TTP0 + length + type + payload` (no CRC) — used to compute the checksum |
| `framebuilder(PRTV, MSGLint, TYPE, MSG, CRCint_high, CRCint_low)` | Builds complete TTP0 frame with CRC bytes appended |

### `src/base-impl/reciever.py`

| Name | Purpose |
|------|---------|
| `CRC16` | Same CRC-16/IBM implementation as transmitter |
| `parser(data, show_debug)` | Splits a raw frame into protocol version, type, length, payload, CRC bytes |
| `check_crc(received_frame, received_crc, show_debug)` | Recomputes CRC over the frame and compares against received CRC |

### `src/base-impl/errcheck.py`

| Name | Purpose |
|------|---------|
| `NoChars` | Exception raised when message length is 0 |
| `MacChars` | Exception raised when message exceeds 31 bytes |
| `checkbuffer(MSGLEN)` | Validates length constraints with `checknochars()` and `checkmaxchars()` |

### `src/base-impl/client.py`

- Connects to `127.0.0.1:65432` over TCP
- Reads input from stdin, encodes as UTF-8
- Validates length via `errcheck.checkbuffer`
- Computes CRC-16 over `TTP0 + length + type + payload`
- Sends full frame over the socket
- Waits for `b'\x01'` (ACK) or `b'\x02'` (NACK) from server

### `src/base-impl/server.py`

- Listens on `127.0.0.1:65432`
- Accepts one TCP connection
- Receives bytes, parses them with `reciever.parser()`
- Verifies CRC with `reciever.check_crc()`
- Sends `ACK = b'1'` if packet is good, `NACK = b'2'` if bad

---

## CRC-16/IBM

Both `transmitter.py` and `reciever.py` include the same `CRC16` class:

| Param | Value | Meaning |
|-------|-------|---------|
| `polynomial` | `0xA001` | Generator polynomial (reversed `0x8005`) |
| `init` | `0xFFFF` | Starting CRC value |
| `xor_out` | `0x0000` | Final XOR applied to the CRC |

Lookup-table implementation for speed.

Typical use:
```python
crc = CRC16()
crc.update(frame_without_crc)
value = crc.digest()      # int, 0..65535
crc.hexdigest()           # e.g. "8F3A"
```

---

## Try It

**Terminal 1 — Start the server:**
```bash
python src/base-impl/server.py
```

**Terminal 2 — Start the client:**
```bash
python src/base-impl/client.py
```

Type a message (max 31 bytes) and hit enter. The server will print the parsed frame and reply with ACK or NACK.

---

## Philosophy

> **Make it work, make it right, make it fast.** — Kent Beck

This is *make it work* stage. It teaches the bones of every protocol you'll ever meet: **magic, length, payload, checksum**. HTTP, MQTT, CAN, USB — same skeleton, more flesh.

---

## License

GNU General Public License v3.0. See `LICENSE` for details.

---

> **Note:** This README was generated by an AI assistant. The code in `src/base-impl/` is human-written.