# Simple Multi-Webhook Wrapper

A minimal and efficient Python wrapper for managing and sending messages to multiple webhooks simultaneously using numeric or string IDs. It includes built-in safeguards, response flashing, and clean custom error descriptions.

## Custom Exceptions

The module imports custom exceptions from an external `exceptions` file:

- **`InvalidURL`**: Raised if the URL string is empty or missing.
- **`AlreadyExists`**: Raised if you try to register a URL on an ID that is already taken.
- **`NoSuchID`**: Raised if you try to send a message using an uninitialized ID.
- **`ContentTooLarge`**: Raised if the text payload exceeds the 2000-character limit.
- **`ConnectionError`**: Network issues or host is completely unreachable.
- **`SchemaError`**: Raised when the URL format misses `http://` or `https://`.
- **`BadRequest`**: Server returned an explicit HTTP `400` error.
- **`InternalServerError`**: Server encountered a critical HTTP `500` error.
- **`HTTPError`**: Triggers for any other non-2xx server responses.

## Core Functions

### `init(url: str, id=1)`
Registers a webhook URL under a unique identifier.
- **Default ID:** `1`
- **Raises:** `InvalidURL` if the URL is empty, `AlreadyExists` if the ID is already registered.

### `send(content: str, ids, statCode: bool = False, flush: bool = False)`
Dispatches a payload string to the webhook registered under the specified `ids`.
- **`ids`**: The target webhook identifier.
- **`statCode`**: If set to `True`, prints the server response status code in the console.
- **`flush`**: If set to `True`, prints the raw text/JSON response returned from the server endpoint.

## Usage Example

```python
import dswebhook as dsw

# 1. Initialize dswebhook with ID 

dsw.init("https://discord.com...", id=1)dsw.init("https://discord.com...", "id="backup_channel")

# 2. Send logs with debugging features enabled
try:
    # Sends a message and prints out status code and server raw response text
dsw.send("System updated successfully!", ids=1, statCode=True, flush=True)

    # Sends a message to the second text channel using a string ID
dsw.send("Alert triggered.", ids="backup_channel")

except dsw.AlreadyExists as e:
    print(f"Configuration conflict: {e}")
except dsw.NoSuchID as e:
    print(f"Targeting error: {e}")
except dsw.HTTPError as e:
    print(f"Server communication failed: {e}")
```
