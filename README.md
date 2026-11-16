# TTP0 - Text Transfer Protocol v0

A minimal custom text transfer protocol implementation in Python.

## Protocol Overview

TTP0 (Text Transfer Protocol version 0) is a simple wire protocol for transferring text messages. Each message is framed with a protocol magic identifier, length byte, payload, and a CRC byte.

## Frame Format

Each TTP0 frame consists of:

```
[PROTOCOL_VERSION: 4 bytes][MSGLEN: 1 byte][MSG: variable][CRC: 1 byte]
```

| Field | Size | Description |
|-------|------|-------------|
| PROTOCOL_VERSION | 4 bytes | Magic identifier `0x54 0x54 0x50 0x30` ("TTP0") |
| MSGLEN | 1 byte | Length of the message payload in bytes (big-endian) |
| MSG | variable | UTF-8 encoded message payload |
| CRC | 1 byte | Checksum byte (currently fixed value `12`) |

## Components

### Constants

- `PROTOCOL_VERSION` - Magic bytes identifying the protocol (`0x54, 0x54, 0x50, 0x30`)
- `CRC` - Checksum value (fixed at `12`)

### Exceptions

- `NoChars` - Raised when an empty message (length 0) is passed to the buffer check

### Functions

#### `checkbuffer(MSGLEN)`
Validates that the message buffer is not empty.

- **Parameters:** `MSGLEN` (int) - Length of the message
- **Returns:** The message string if valid
- **Raises:** `NoChars` if `MSGLEN == 0`

#### `framebuilder(PRTV, MSGLint, MSG, CRCint)`
Constructs a TTP0 frame from the individual components.

- **Parameters:**
  - `PRTV` (bytes) - Protocol version magic bytes
  - `MSGLint` (int) - Message length
  - `MSG` (bytes) - UTF-8 encoded message
  - `CRCint` (int) - CRC value
- **Returns:** The function currently returns a reference to `framebuilder` itself (not the frame)
- **Side effects:** Prints type information and the constructed frame bytes to stdout

## Usage

The program reads a message from standard input, validates it, and builds a TTP0 frame.

### Input
- A text message via stdin (maximum 31 characters)

### Output
- Type information debug prints
- The constructed frame as bytes

## Constraints

- Maximum message length: 31 characters (1 byte limits payload length to 0-255, but the code enforces 31)
- Empty messages are rejected with `NoChars` exception
- CRC is currently a fixed placeholder value

## Source Files

- `src/main.py` - Protocol implementation
- `src/text.txt` - Sample text data