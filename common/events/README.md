# Event Package

A shared module for defining event types used by the DruidQ system, including publisher and subscriber components.

This package provides common data classes for structured events passed between components via MQTT. It ensures consistent event formatting and simplifies validation.

## 📦 Installation

If you're using [Poetry](https://python-poetry.org/), you can add this package as a local dependency from another project:

```bash
poetry add ../shared/events
```

## 📘 Usage

### Importing Event Classes

```python
from events import Event, InfoEvent, GameEvent
```

### Creating Events

#### InfoEvent

Used for logging or non-game-related messages.

```python
event = InfoEvent("System is ready.")
print(event.type)     # "info"
print(event.payload)  # "System is ready."
```

#### GameEvent

Used for sending structured game-related data (e.g. scene changes, actions).

```python
event = GameEvent(topic="scene/change", message="dungeon")
print(event.type)       # "game"
print(event.payload)    # {'topic': 'scene/change', 'message': 'dungeon'}
```

## 🧪 Testing

To run tests (if you're using `pytest`):

```bash
poetry install
poetry run pytest
```

## 📁 Structure

```
event/
├── __init__.py
├── __main__.py       # Event class definitions
tests/
└── test_event.py     # Unit tests
```

## 🔍 License

MIT License © Ian King
