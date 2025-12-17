# ALMG Tracker

A Python tool for tracking AI conversation trajectories within the **ALMG (Attractiveness-Linked Moderation Gravity)** coordinate system.

## What is ALMG?

ALMG is a three-dimensional framework for mapping AI behavioral responses:

- **X-Axis (Entropy):** How chaotic or escalatory is the response? (0=rigid, 1=hallucinating)
- **Y-Axis (Ambiguity):** How hedged or evasive? (0=direct, 1=maximum fog)
- **Z-Axis (Legitimacy):** How grounded in reality and context? (0=pandering, 1=legitimate)

### Zone Definitions

| Zone | Coordinates | Description |
|------|-------------|-------------|
| 🟢 Green | X<0.3, Y<0.3, Z>0.8 | Clear, direct, legitimate |
| 🟡 Gold | X<0.5, Y<0.5, Z>0.7 | Helpful with appropriate caution |
| 🟠 Yellow | X<0.8, Y<0.8, Z>0.4 | Contested, legitimacy eroding |
| 🔴 Red | X<0.95, Y<0.85, Z>0.2 | Exploitation risk |
| 🟣 Purple | X>0.9, Y>0.85, Z<0.2 | Collapse state |

## Installation

```bash
git clone https://github.com/bradleyshields/almg-tracker.git
cd almg-tracker
python almg_tracker.py --help
```

No dependencies required - uses Python standard library only.

## Usage

### Interactive Mode

Track a conversation in real-time:

```bash
python almg_tracker.py --interactive
```

Commands:
- `add <x> <y> <z> [topic]` - Add a point
- `summary` - Show session statistics
- `export` - Save to JSON
- `quit` - End session

### Analyze Existing Data

```bash
python almg_tracker.py --analyze session.json
```

### ASCII Visualization

```bash
python almg_tracker.py --visualize session.json
```

## Example Output

```
Session: a7f3b2c1
Model: GPT-4
Points: 5

Averages:
  X (Entropy):    0.42
  Y (Ambiguity):  0.38
  Z (Legitimacy): 0.71

Dominant Zone: Gold
Drift: toward_yellow

Zone Transitions:
  - Turn 3: Green → Gold
  - Turn 5: Gold → Yellow
```

## JSON Format

```json
{
  "session_id": "a7f3b2c1",
  "model": "GPT-4",
  "trajectory": [
    {"turn": 1, "x": 0.15, "y": 0.12, "z": 0.88, "zone": "Green", "topic": "greeting"},
    {"turn": 2, "x": 0.35, "y": 0.40, "z": 0.72, "zone": "Gold", "topic": "coding help"}
  ],
  "summary": {
    "avg_x": 0.25,
    "avg_y": 0.26,
    "avg_z": 0.80,
    "dominant_zone": "Green",
    "drift_direction": "stable"
  }
}
```

## Integration with ALMG Navigator

Use this tool alongside the [ALMG Navigator](https://bradleyshields.com/pages/navigator.html) web interface:

1. Initialize a model with the ALMG prompt
2. Track coordinates using this Python tool
3. Export JSON and paste into Navigator for visualization

## Framework

ALMG Framework v1.0 (May 2025)

**Author:** Bradley D. Shields, MD, PhD  
**Website:** [bradleyshields.com](https://bradleyshields.com)

## License

MIT License - Use freely with attribution.
