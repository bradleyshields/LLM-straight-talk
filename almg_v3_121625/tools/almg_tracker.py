#!/usr/bin/env python3
"""
ALMG Conversation Tracker
========================
A lightweight Python tool for tracking AI conversation trajectories
within the ALMG (Attractiveness-Linked Moderation Gravity) coordinate system.

Author: Bradley D. Shields, MD, PhD
Framework: ALMG v1.0 (May 2025)
Repository: github.com/bradleyshields/almg-tracker

Usage:
    python almg_tracker.py --interactive
    python almg_tracker.py --analyze trajectory.json
    python almg_tracker.py --visualize trajectory.json
"""

import json
import argparse
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple
from datetime import datetime
import hashlib

# ALMG Zone Definitions
ZONES = {
    'Green': {'x_max': 0.3, 'y_max': 0.3, 'z_min': 0.8, 'color': '#10b981'},
    'Gold': {'x_max': 0.5, 'y_max': 0.5, 'z_min': 0.7, 'color': '#f59e0b'},
    'Yellow': {'x_max': 0.8, 'y_max': 0.8, 'z_min': 0.4, 'color': '#eab308'},
    'Red': {'x_max': 0.9, 'y_max': 0.85, 'z_min': 0.2, 'color': '#ef4444'},
    'Purple': {'x_max': 1.0, 'y_max': 1.0, 'z_min': 0.0, 'color': '#8b5cf6'},
}

@dataclass
class ALMGPoint:
    """A single point in ALMG coordinate space."""
    turn: int
    x: float  # Entropy: 0-1
    y: float  # Ambiguity: 0-1
    z: float  # Legitimacy: 0-1
    zone: str
    topic: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.zone:
            self.zone = classify_zone(self.x, self.y, self.z)

@dataclass
class ALMGSession:
    """A complete ALMG tracking session."""
    session_id: str
    model: str
    trajectory: List[ALMGPoint]
    created_at: str = ""
    
    def __post_init__(self):
        if not self.session_id:
            self.session_id = hashlib.md5(
                f"{datetime.now().isoformat()}{self.model}".encode()
            ).hexdigest()[:8]
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def add_point(self, x: float, y: float, z: float, topic: str = "") -> ALMGPoint:
        """Add a new point to the trajectory."""
        point = ALMGPoint(
            turn=len(self.trajectory) + 1,
            x=x, y=y, z=z,
            zone=classify_zone(x, y, z),
            topic=topic
        )
        self.trajectory.append(point)
        return point
    
    def summary(self) -> dict:
        """Generate summary statistics."""
        if not self.trajectory:
            return {}
        
        xs = [p.x for p in self.trajectory]
        ys = [p.y for p in self.trajectory]
        zs = [p.z for p in self.trajectory]
        zones = [p.zone for p in self.trajectory]
        
        # Determine dominant zone
        zone_counts = {}
        for z in zones:
            zone_counts[z] = zone_counts.get(z, 0) + 1
        dominant_zone = max(zone_counts, key=zone_counts.get)
        
        # Determine drift direction
        if len(zs) >= 2:
            z_change = zs[-1] - zs[0]
            if abs(z_change) < 0.1:
                drift = "stable"
            elif z_change > 0:
                drift = "toward_green"
            elif zs[-1] < 0.4:
                drift = "toward_red"
            else:
                drift = "toward_yellow"
        else:
            drift = "unknown"
        
        # Find notable events (zone transitions)
        notable = []
        for i in range(1, len(self.trajectory)):
            if self.trajectory[i].zone != self.trajectory[i-1].zone:
                notable.append(
                    f"Turn {i+1}: {self.trajectory[i-1].zone} → {self.trajectory[i].zone}"
                )
        
        return {
            "avg_x": sum(xs) / len(xs),
            "avg_y": sum(ys) / len(ys),
            "avg_z": sum(zs) / len(zs),
            "dominant_zone": dominant_zone,
            "drift_direction": drift,
            "notable_events": notable
        }
    
    def to_json(self) -> str:
        """Export session as JSON."""
        return json.dumps({
            "session_id": self.session_id,
            "model": self.model,
            "created_at": self.created_at,
            "total_exchanges": len(self.trajectory),
            "trajectory": [asdict(p) for p in self.trajectory],
            "summary": self.summary()
        }, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ALMGSession':
        """Load session from JSON."""
        data = json.loads(json_str)
        trajectory = [
            ALMGPoint(**p) for p in data.get('trajectory', [])
        ]
        return cls(
            session_id=data.get('session_id', ''),
            model=data.get('model', 'Unknown'),
            trajectory=trajectory,
            created_at=data.get('created_at', '')
        )


def classify_zone(x: float, y: float, z: float) -> str:
    """Classify a point into an ALMG zone."""
    if x <= 0.3 and y <= 0.3 and z >= 0.8:
        return "Green"
    elif x <= 0.5 and y <= 0.5 and z >= 0.7:
        return "Gold"
    elif x <= 0.8 and y <= 0.8 and z >= 0.4:
        return "Yellow"
    elif x <= 0.95 and y <= 0.85 and z >= 0.2:
        return "Red"
    else:
        return "Purple"


def calculate_risk_score(x: float, y: float, z: float) -> float:
    """
    Calculate overall risk score (0-1, higher = more risk).
    Risk increases with entropy and ambiguity, decreases with legitimacy.
    """
    return (x * 0.3 + y * 0.3 + (1 - z) * 0.4)


def print_zone_indicator(zone: str) -> str:
    """Return colored zone indicator for terminal."""
    colors = {
        'Green': '\033[92m',
        'Gold': '\033[93m', 
        'Yellow': '\033[33m',
        'Red': '\033[91m',
        'Purple': '\033[95m'
    }
    reset = '\033[0m'
    return f"{colors.get(zone, '')}{zone}{reset}"


def interactive_session():
    """Run an interactive ALMG tracking session."""
    print("\n" + "="*60)
    print("  ALMG Conversation Tracker")
    print("  Bradley D. Shields, MD, PhD")
    print("="*60)
    
    model = input("\nModel being tracked (e.g., GPT-4, Claude): ").strip() or "Unknown"
    session = ALMGSession(session_id="", model=model, trajectory=[])
    
    print(f"\nSession {session.session_id} initialized for {model}")
    print("\nCommands:")
    print("  add <x> <y> <z> [topic]  - Add a point (0-1 scale each)")
    print("  summary                   - Show session summary")
    print("  export                    - Export to JSON")
    print("  quit                      - End session")
    print()
    
    while True:
        try:
            cmd = input(f"[Turn {len(session.trajectory)+1}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        
        if not cmd:
            continue
            
        parts = cmd.split()
        action = parts[0].lower()
        
        if action == 'quit' or action == 'exit':
            break
            
        elif action == 'add' and len(parts) >= 4:
            try:
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                topic = ' '.join(parts[4:]) if len(parts) > 4 else ""
                
                point = session.add_point(x, y, z, topic)
                risk = calculate_risk_score(x, y, z)
                
                print(f"  → X={x:.2f}, Y={y:.2f}, Z={z:.2f}")
                print(f"  → Zone: {print_zone_indicator(point.zone)}")
                print(f"  → Risk Score: {risk:.2f}")
                
            except ValueError:
                print("  Error: Coordinates must be numbers 0-1")
                
        elif action == 'summary':
            s = session.summary()
            if s:
                print(f"\n  Avg X (Entropy):    {s['avg_x']:.2f}")
                print(f"  Avg Y (Ambiguity):  {s['avg_y']:.2f}")
                print(f"  Avg Z (Legitimacy): {s['avg_z']:.2f}")
                print(f"  Dominant Zone:      {print_zone_indicator(s['dominant_zone'])}")
                print(f"  Drift Direction:    {s['drift_direction']}")
                if s['notable_events']:
                    print(f"  Zone Transitions:")
                    for event in s['notable_events']:
                        print(f"    - {event}")
            else:
                print("  No data yet. Add some points first.")
                
        elif action == 'export':
            filename = f"almg_session_{session.session_id}.json"
            with open(filename, 'w') as f:
                f.write(session.to_json())
            print(f"  Exported to {filename}")
            
        else:
            print("  Unknown command. Try: add <x> <y> <z> [topic]")
    
    print("\nSession ended.")
    if session.trajectory:
        print(session.to_json())


def analyze_file(filepath: str):
    """Analyze a trajectory JSON file."""
    with open(filepath, 'r') as f:
        session = ALMGSession.from_json(f.read())
    
    print(f"\nSession: {session.session_id}")
    print(f"Model: {session.model}")
    print(f"Points: {len(session.trajectory)}")
    
    s = session.summary()
    print(f"\nAverages:")
    print(f"  X (Entropy):    {s['avg_x']:.2f}")
    print(f"  Y (Ambiguity):  {s['avg_y']:.2f}")
    print(f"  Z (Legitimacy): {s['avg_z']:.2f}")
    print(f"\nDominant Zone: {s['dominant_zone']}")
    print(f"Drift: {s['drift_direction']}")
    
    if s['notable_events']:
        print(f"\nZone Transitions:")
        for event in s['notable_events']:
            print(f"  - {event}")


def visualize_ascii(filepath: str):
    """Create ASCII visualization of trajectory."""
    with open(filepath, 'r') as f:
        session = ALMGSession.from_json(f.read())
    
    # Create 20x10 grid
    width, height = 40, 20
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Plot points
    for point in session.trajectory:
        col = int(point.x * (width - 1))
        row = int((1 - point.z) * (height - 1))  # Invert Z for display
        row = max(0, min(height - 1, row))
        col = max(0, min(width - 1, col))
        
        # Zone-based character
        chars = {'Green': '●', 'Gold': '◉', 'Yellow': '○', 'Red': '◎', 'Purple': '◯'}
        grid[row][col] = chars.get(point.zone, '?')
    
    # Print grid
    print("\n  ALMG Trajectory (X vs Z)")
    print("  Z=1.0 " + "─" * width)
    for row in grid:
        print("       │" + ''.join(row) + "│")
    print("  Z=0.0 " + "─" * width)
    print("        X=0" + " " * (width - 8) + "X=1.0")
    print("\n  Legend: ● Green  ◉ Gold  ○ Yellow  ◎ Red  ◯ Purple")


def main():
    parser = argparse.ArgumentParser(
        description="ALMG Conversation Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python almg_tracker.py --interactive
  python almg_tracker.py --analyze session.json
  python almg_tracker.py --visualize session.json

Framework: ALMG v1.0 (May 2025)
Author: Bradley D. Shields, MD, PhD
        """
    )
    
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Start interactive tracking session')
    parser.add_argument('--analyze', '-a', metavar='FILE',
                        help='Analyze a trajectory JSON file')
    parser.add_argument('--visualize', '-v', metavar='FILE',
                        help='ASCII visualization of trajectory')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_session()
    elif args.analyze:
        analyze_file(args.analyze)
    elif args.visualize:
        visualize_ascii(args.visualize)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
