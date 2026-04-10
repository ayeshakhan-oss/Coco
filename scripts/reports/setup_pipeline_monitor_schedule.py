"""
Setup Script: Register Windows Task Scheduler Tasks
====================================================
Registers two automated tasks for the weekly pipeline monitor:
  - Monday 10:30am
  - Friday 3:00pm

Run once: python scripts/reports/setup_pipeline_monitor_schedule.py
"""

import subprocess
import sys
import os

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "weekly_pipeline_monitor.py")
PYTHON_PATH = sys.executable

def register_tasks():
    """Register both tasks in Windows Task Scheduler."""

    print("=" * 70)
    print("PIPELINE MONITOR — Task Scheduler Setup")
    print("=" * 70)
    print()

    # Task 1: Monday 10:30am
    print("[Task 1] Registering Monday 10:30am task...")
    try:
        cmd1 = [
            "schtasks", "/create",
            "/tn", "CocoPipelineMonitor_Monday",
            "/tr", f'"{PYTHON_PATH}" "{SCRIPT_PATH}"',
            "/sc", "WEEKLY",
            "/d", "MON",
            "/st", "10:30",
            "/f"
        ]
        subprocess.run(cmd1, check=True, capture_output=True, text=True)
        print("  ✓ Monday task registered")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed to register Monday task: {e.stderr}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    print()

    # Task 2: Friday 3:00pm
    print("[Task 2] Registering Friday 3:00pm task...")
    try:
        cmd2 = [
            "schtasks", "/create",
            "/tn", "CocoPipelineMonitor_Friday",
            "/tr", f'"{PYTHON_PATH}" "{SCRIPT_PATH}"',
            "/sc", "WEEKLY",
            "/d", "FRI",
            "/st", "15:00",
            "/f"
        ]
        subprocess.run(cmd2, check=True, capture_output=True, text=True)
        print("  ✓ Friday task registered")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed to register Friday task: {e.stderr}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    print()
    print("=" * 70)
    print("✓ Both tasks registered successfully!")
    print()
    print("To verify, run: schtasks /query /tn CocoPipelineMonitor*")
    print()
    print("To remove tasks later, run:")
    print("  schtasks /delete /tn CocoPipelineMonitor_Monday /f")
    print("  schtasks /delete /tn CocoPipelineMonitor_Friday /f")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = register_tasks()
    sys.exit(0 if success else 1)
