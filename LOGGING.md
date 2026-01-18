# Enhanced Logging in docx-tex-validator

This document describes the enhanced logging features added to docx-tex-validator that provide comprehensive visibility into LLM interactions.

## Overview

The validator now includes detailed debug logging that captures:

1. **Full prompts** sent to the LLM (complete conversation transcript)
2. **Full responses** received from the LLM
3. **Token usage** information for each request
4. **Response metadata** including HTTP response details

This enhanced logging makes it much easier to:
- Debug validation issues
- Understand what the LLM is seeing
- Track token consumption
- Monitor API interactions

## Enabling Debug Logging

### Python Code

To enable debug logging in your Python code:

```python
import logging
from docx_tex_validator import DocxValidator, ValidationSpec

# Configure logging to show DEBUG messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create validator and use normally
validator = DocxValidator(
    backend="openai",
    model_name="gpt-4o",  # New default with 128k context window
    api_key="your_api_key"
)

# Validate document - debug logs will show all LLM interactions
report = validator.validate("document.docx", specifications)
```

### Command Line

For command-line usage, you can enable debug logging by setting the logging level:

```bash
# Set PYTHONLOGGING environment variable
export PYTHONLOGGING=DEBUG

# Or configure logging in your shell
python -c "import logging; logging.basicConfig(level=logging.DEBUG); \
from docx_tex_validator.cli import main; main()" \
validate document.docx -s specs.json
```

## What Gets Logged

### 1. Document Context Setup

When the validator sets up the document context, you'll see:

```
================================================================================
LLM REQUEST - Document Context Setup
================================================================================
Prompt:

I will provide you with a document structure to analyze. After I provide the document, 
I will ask you a series of validation questions about it. Please analyze and remember 
this document structure.

Document Structure:
{
  "metadata": {
    "title": "Sample Document",
    "author": "Test Author"
  },
  "paragraphs": [
    "This is paragraph one",
    "This is paragraph two"
  ]
}

Please confirm you have received and understood the document structure...
--------------------------------------------------------------------------------
Response received
Response data: Document structure received and ready for validation.
Token usage: {'prompt_tokens': 245, 'completion_tokens': 12}
Response metadata: {'model': 'gpt-4o', 'finish_reason': 'stop'}
================================================================================
```

### 2. Validation Requests

For each validation specification, you'll see:

```
================================================================================
LLM REQUEST - Validation (with context)
================================================================================
Specification: Has Title
Prompt:

Now validate this requirement:

Requirement Name: Has Title
Description: Document must contain a title in the metadata
Category: metadata

Does the document meet this requirement? Respond with:
1. "PASS" or "FAIL"
2. A confidence score between 0.0 and 1.0
3. A brief explanation of your reasoning
--------------------------------------------------------------------------------
Response received
Response data: Result: PASS
Confidence: 1.0
Reasoning: The document contains a title 'Sample Document' in its metadata.
Token usage: {'prompt_tokens': 78, 'completion_tokens': 24}
Response metadata: {'model': 'gpt-4o', 'finish_reason': 'stop'}
================================================================================
```

### 3. Backend Information

At the backend level, you'll also see:

```
DEBUG: Backend run_sync called with model: gpt-4o
DEBUG: HTTP/API Response metadata: {'model': 'gpt-4o', 'finish_reason': 'stop'}
```

## Log Filtering

You can filter logs to show only specific components:

```python
import logging

# Show only validator logs
logging.getLogger('docx_tex_validator.validator').setLevel(logging.DEBUG)

# Show only backend logs
logging.getLogger('docx_tex_validator.backends.openai').setLevel(logging.DEBUG)

# Show all docx_tex_validator logs
logging.getLogger('docx_tex_validator').setLevel(logging.DEBUG)
```

## Logging to File

To capture debug logs to a file:

```python
import logging

# Configure file handler
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('validator_debug.log'),
        logging.StreamHandler()  # Also log to console
    ]
)

# Run validation - logs will be saved to validator_debug.log
validator = DocxValidator(api_key="your_api_key")
report = validator.validate("document.docx", specs)
```

## New Default Model: gpt-4o

The default model has been changed from `gpt-4o-mini` to `gpt-4o`:

- **Previous default**: `gpt-4o-mini` (128k context window, cost-optimized)
- **New default**: `gpt-4o` (128k context window, higher quality)

The `gpt-4o` model provides:
- Larger context window (128k tokens)
- Better reasoning capabilities
- More accurate validation results
- Better handling of complex documents

You can still use other models by specifying the `model_name` parameter:

```python
# Use gpt-4o-mini for cost savings
validator = DocxValidator(model_name="gpt-4o-mini")

# Use gpt-4-turbo for maximum context
validator = DocxValidator(model_name="gpt-4-turbo")

# Use gpt-4o (default - no need to specify)
validator = DocxValidator()
```

## Example: Full Logging Script

See `examples/demo_logging.py` for a complete example that demonstrates the enhanced logging features.

## Troubleshooting

### No Debug Logs Appearing

If you don't see debug logs:

1. Verify logging level is set to DEBUG:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Check that you're looking at the right logger:
   ```python
   logger = logging.getLogger('docx_tex_validator')
   logger.setLevel(logging.DEBUG)
   ```

3. Ensure logging is configured before importing the validator:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)  # Do this first
   from docx_tex_validator import DocxValidator  # Then import
   ```

### Too Much Output

If debug logs are too verbose, you can:

1. Use INFO level for less detail:
   ```python
   logging.basicConfig(level=logging.INFO)
   ```

2. Filter specific loggers:
   ```python
   # Only show validator logs, not backend logs
   logging.getLogger('docx_tex_validator.validator').setLevel(logging.DEBUG)
   logging.getLogger('docx_tex_validator.backends').setLevel(logging.INFO)
   ```

## Security Note

Be careful when sharing debug logs as they contain:
- Full document structure (may contain sensitive information)
- API interactions and responses
- Token usage patterns

Always sanitize logs before sharing them publicly.
