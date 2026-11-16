# TTP0 - Text Transfer Protocol v0

A simple custom protocol that wraps a text message in a binary frame with a CRC16 checksum so a receiver can verify the message arrived intact.

## Frame Format

```
TTP0 + length + text + CRC16
```

```
┌─────────────┬────────┬──────────────┬──────────────┐
│  "TTP0"     │ length │  text        │  CRC16       │
│  (4 bytes)  │(1 byte)│  (N bytes)   │  (2 bytes)   │
└─────────────┴────────┴──────────────┴──────────────┘
```

| Field | Size | Description |
|-------|------|-------------|
| `TTP0` | 4 bytes | Protocol magic `0x54 0x54 0x50 0x30` ("TTP0"). Identifies this as a TTP0 frame. |
| `length` | 1 byte | Length of the text payload in bytes (big-endian, max 255). |
| `text` | N bytes | The message, UTF-8 encoded. |
| `CRC16` | 2 bytes | CRC-16/IBM checksum of `TTP0 + length + text`, big-endian (high byte first). |

### Example

Message: `Hi` (2 bytes)

```
54 54 50 30 02 48 69 <CRC_hi> <CRC_lo>
└──────────┘ └┘ └────┘ └──────────┘
  TTP0     len  "Hi"    CRC16
```

## How It Works

1. Read a line of text from stdin.
2. Encode it as UTF-8 and measure its length.
3. Build the frame **without** CRC: `TTP0 + length + text`.
4. Run CRC-16/IBM over those bytes.
5. Split the 16-bit CRC into a high byte and low byte.
6. Append them to build the final frame: `TTP0 + length + text + CRC16`.
7. Print the frame bytes.

## CRC-16/IBM

The `CRC16` class implements CRC-16/IBM with these defaults:

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `polynomial` | `0xA001` | Generator polynomial (reversed `0x8005`). |
| `init` | `0xFFFF` | Starting CRC value. |
| `xor_out` | `0x0000` | Final XOR applied to the CRC. |

It uses a precomputed 256-entry lookup table for speed. Typical use:

```python
crc = CRC16()
crc.update(frame_without_crc)
value = crc.digest()      # int, 0..65535
crc.hexdigest()           # e.g. "8F3A"
```

## Code Reference (`src/main.py`)

| Name | Purpose |
|------|---------|
| `CRC16` | CRC-16/IBM class. Methods: `reset()`, `update(data)`, `digest()`, `hexdigest()`. |
| `NoChars` | Exception raised when the message is empty. |
| `checkbuffer(MSGLEN)` | Raises `NoChars` if `MSGLEN == 0`, otherwise returns the message. |
| `framebuildernocrc(PRTV, MSGLint, MSG)` | Builds `PRTV + MSGLbytes + MSG` (no CRC) and returns those bytes. Used to compute the CRC. |
| `framebuilder(PRTV, MSGLint, MSG, CRCint_high, CRCint_low)` | Builds the full frame with the two CRC bytes appended. |
| `PROTOCOL_VERSION` | The magic bytes `0x54 0x54 0x50 0x30`. |
| `MESSAGE` / `UTF8MSG` / `MSGLEN` | Input text, its UTF-8 bytes, and its length. |

## Run

```bash
python src/main.py
```

Type a message and press enter. The program prints debug type info and the final framed bytes, e.g.:

```
b'TTP0\x02Hi\x8f\xc3'
```

## Notes & Known Issues

- `checkbuffer` returns `MESSAGE` (a global), not `MSGLEN`; it only validates the length.
- `framebuilder` returns the function `framebuilder` instead of the `frame` it built.
- The "31 characters" message is misleading: a 1-byte length field allows up to 255 bytes.

## Files

- `src/main.py` - Protocol implementation.
- `src/text.txt` - Sample text.