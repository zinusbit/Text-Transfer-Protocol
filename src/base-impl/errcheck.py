class NoChars(Exception):
    """Raised when message buffer is empty."""
    pass
class MacChars(Exception):
    """Raised when message exceeds maximum length."""
    pass

class checkbuffer:
    """Validate message length constraints."""

    def __init__(self, MSGLEN):
        self.MSGLEN = MSGLEN

    def checknochars(self):
        """Raise NoChars if message length is zero."""
        if self.MSGLEN == 0:
            raise NoChars("No Chars in the buffer")
        return self.MSGLEN
    
    def checkmaxchars(self):
        """Raise MacChars if message exceeds 31 bytes."""
        if self.MSGLEN > 31:
            raise MacChars("Maximum number of chars exceeded")
        return self.MSGLEN