# File Organizer Agent

An intelligent file organizer powered by LangGraph and LLMs. Automatically categorizes and organizes files into folders based on their type.

## Features

- **Multi-LLM Support** - Switch between OpenAI and Groq with a single env var
- **Per-Agent Configuration** - Use different LLMs for different agents
- **Extensible Provider System** - Add new LLM providers with ~5 lines of code
- **Local Filesystem** - Organizes files on your local machine
- **LangGraph Workflow** - State machine architecture for reliable execution
- **Configurable Categories** - Images, Documents, Code, and more

## Architecture

```
┌────────────┐    ┌─────────────────┐    ┌────────┐    ┌─────────┐
│  pick_file │───▶│ decide_category │───▶│  move  │───▶│ observe │
└────────────┘    │    (LLM call)   │    └────────┘    └────┬────┘
                  └─────────────────┘                       │
                          ▲                                 │
                          └─────────── loop ────────────────┘
```

**Workflow:**
1. **pick_file** - Selects the next file from input directory
2. **decide_category** - Uses LLM to determine file category
3. **move** - Moves file to appropriate category folder
4. **observe** - Tracks progress, loops or terminates

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key or Groq API key

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd agenticAI

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Create environment file
cp .env.example .env

# Add your API key to .env
```

## Configuration

Edit `.env` to configure the agent:

### LLM Settings

```env
# Default LLM provider: "openai" or "groq"
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0

# API Keys
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
```

### Per-Agent Overrides

```env
# Use different LLM for categorizer agent
CATEGORIZER_LLM_PROVIDER=groq
CATEGORIZER_LLM_MODEL=llama-3.3-70b-versatile
CATEGORIZER_LLM_TEMPERATURE=0
```

### Directory Settings

```env
SOURCE_DIR=./input_files    # Files to organize
DEST_DIR=./output_files     # Organized output
```

## Usage

### Basic Usage

```bash
# Place files in input_files/
# Run the agent
uv run python run.py
```

### Output

Files are organized into category folders:
```
output_files/
├── Images/
│   ├── photo.jpg
│   └── screenshot.png
├── Documents/
│   ├── report.pdf
│   └── notes.txt
├── Code/
│   └── script.py
└── Others/
    └── unknown.xyz
```

## Switching LLMs

### Use OpenAI

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
```

### Use Groq

```env
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
```

### Mix Providers (Per-Agent)

```env
# Default to OpenAI
LLM_PROVIDER=openai

# But use Groq for categorization (faster/cheaper)
CATEGORIZER_LLM_PROVIDER=groq
```

## Adding New LLM Providers

Add a new provider in `tools/llm_factory.py`:

```python
def _create_anthropic(model=None, temperature=0, **kwargs):
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model=model or "claude-3-sonnet-20240229",
        temperature=temperature,
        **kwargs
    )
register_provider("anthropic", _create_anthropic)
```

Then use it:
```env
LLM_PROVIDER=anthropic
```

## Project Structure

```
agenticAI/
├── agent/
│   ├── graph.py          # LangGraph workflow definition
│   └── state.py          # Agent state schema
├── config/
│   └── settings.py       # Configuration and validation
├── tools/
│   ├── llm_factory.py    # Multi-LLM factory
│   ├── llm.py            # Default LLM instance
│   └── blob_tools.py     # File operations
├── input_files/          # Source files to organize
├── output_files/         # Organized output
├── run.py                # Entry point
├── pyproject.toml        # Dependencies
├── .env                  # Configuration
└── .env.example          # Configuration template
```

## How It Works

### LangGraph State Machine

The agent uses LangGraph to manage a state machine workflow:

1. **State** (`agent/state.py`):
   ```python
   class AgentState(TypedDict):
       files: List[str]          # Remaining files
       current_file: str         # Current file
       category: str             # Decided category
       step: int                 # Step counter
   ```

2. **Nodes** (`agent/graph.py`):
   - Each node is a function that receives state and returns updated state
   - The `decide_category` node calls the LLM

3. **Edges**:
   - Linear flow: pick_file → decide_category → move → observe
   - Conditional loop: observe → pick_file (if files remain)

### LLM Factory

The factory pattern (`tools/llm_factory.py`) enables:
- Runtime provider selection
- Easy addition of new providers
- Consistent interface across all LLMs
