# Simple Multi-Webhook Wrapper

A minimal and efficient Python wrapper for managing and sending messages to single or multiple Discord webhooks simultaneously using numeric or string IDs. It includes built-in safeguards, response flushing, and clean custom error descriptions.

## Exceptions

- **`InvalidURL`**: Raised if the URL string is empty, missing, or `send()` is called before `init()`.
- **`AlreadyExists`**: Raised if you try to register a URL on an ID that is already taken.
- **`NoSuchID`**: Raised if you try to send a message using an uninitialized ID.
- **`CantBeEmpty`**: Raised if the message `content` or the `ids` list is empty.
- **`ContentTooLarge`**: Raised if the text payload exceeds the 2000-character limit.
- **`ConnectionError`**: Network issues or host is completely unreachable.
- **`SchemaError`**: Raised when the URL format misses `http://` or `https://`.
- **`TimeOut`**: Raised when the request exceeds the specified `timeout` limit.
- **`LimitReached`**: Raised when the Discord webhook rate limit is exceeded (HTTP `429`).
- **`BadRequest`**: Server returned an explicit HTTP `400` error.
- **`InternalServerError`**: Server encountered a critical HTTP `500` error.
- **`HTTPError`**: Triggers for any other non-2xx server responses.
- **`UnexpectedError`**: Raised for any other unexpected network or request errors.

## Core Functions

### `init(url: str, id=1, avatar_url: str = None, username: str = None)`
Registers a webhook URL under a unique identifier with optional custom profile overrides.
- **Default ID:** `1`
- **Raises:** `InvalidURL` if the URL is empty, `AlreadyExists` if the ID is already registered.

### `send(content: str, ids, timeout: int = 10, wavatar: bool = False, wusername: bool = False, statCode: bool = False, flush: bool = False)`
Dispatches a text payload to a single webhook or multiple webhooks registered under the specified `ids`.
- **`content`**: The text message to send (up to 2000 characters).
- **`ids`**: A single webhook identifier (`int` or `str`) or a `list` of identifiers (e.g., `[1, "backup_channel"]`).
- **`timeout`**: Maximum time in seconds to wait for a server response (default: `10`).
- **`wavatar`**: If set to `True`, sends the message using the custom avatar URL configured for that webhook ID.
- **`wusername`**: If set to `True`, sends the message using the custom username configured for that webhook ID.
- **`statCode`**: If set to `True`, prints the server response status code in the console.
- **`flush`**: If set to `True`, prints the raw text/JSON response returned from the server endpoint.

## Usage Example

```python
import dswebhook as dsw

# 1. Initialize dswebhook with numeric or string IDs
dsw.init("https://discord.com...", id=1)
dsw.init("https://discord.com...", id="backup_channel")

# 2. Send logs with debugging features enabled
try:
    # Sends a message to a single webhook and prints status code and raw response
    dsw.send("System updated successfully!", ids=1, statCode=True, flush=True)

    # Sends a message to multiple webhooks at once using a list of IDs
    dsw.send("Alert triggered.", ids=[1, "backup_channel"])

except dsw.AlreadyExists as e:
    print(f"Configuration conflict: {e}")
except dsw.NoSuchID as e:
    print(f"Targeting error: {e}")
except dsw.LimitReached as e:
    print(f"Rate limit hit: {e}")
except dsw.HTTPError as e:
    print(f"Server communication failed: {e}")
```
