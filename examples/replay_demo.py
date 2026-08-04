"""
Track Digital Operations Sandbox (TDOS)

replay_demo.py

Example demonstrating the TDOS Replay Engine.
"""

from tdos.interfaces.replay_api import ReplayAPI
from tdos.models.asset import RailwayAsset


def main() -> None:

    replay = ReplayAPI()

    replay.start()

    # ======================================================
    # Step 1
    # ======================================================

    asset = RailwayAsset(
        asset_id="AST-001",
        asset_type="RAIL",
        health_score=98.0,
        degradation_rate=0.05,
        age_days=0,
    )

    replay.record(
        step=1,
        assets=[asset],
    )

    # ======================================================
    # Step 2
    # ======================================================

    asset = asset.model_copy(
        update={
            "health_score": 97.8,
            "age_days": 1,
        }
    )

    replay.record(
        step=2,
        assets=[asset],
    )

    # ======================================================
    # Step 3
    # ======================================================

    asset = asset.model_copy(
        update={
            "health_score": 97.6,
            "age_days": 2,
        }
    )

    replay.record(
        step=3,
        assets=[asset],
    )

    replay.stop()

    # ======================================================
    # Replay Summary
    # ======================================================

    print("\nReplay Summary\n")

    print(replay.summary())

    print("\nRecorded Frames\n")

    for frame in replay.frames():

        print(
            f"Step {frame.step} | "
            f"Assets: {len(frame.assets)} | "
            f"Timestamp: {frame.timestamp}"
        )


if __name__ == "__main__":

    main()
