"""
Track Digital Operations Sandbox (TDOS)

test_replay.py

Tests for the TDOS Replay Engine.
"""

from tdos.models.asset import RailwayAsset
from tdos.replay.replay_engine import ReplayEngine

# ==========================================================
# Test Asset
# ==========================================================


def create_asset() -> RailwayAsset:
    """
    Create a sample railway asset.
    """

    return RailwayAsset(
        asset_id="AST-001",
        asset_name="Test Rail",
        asset_type="RAIL",
        latitude=11.0168,
        longitude=76.9558,
        kilometer_post=12.5,
        health_score=98.0,
        degradation_rate=0.05,
        age_days=5,
    )


# ==========================================================
# Replay Engine Creation
# ==========================================================


def test_replay_engine_creation():

    engine = ReplayEngine()

    assert engine is not None


# ==========================================================
# Start Recording
# ==========================================================


def test_replay_start():

    engine = ReplayEngine()

    engine.start()

    assert engine.started_at is not None


# ==========================================================
# Record Frame
# ==========================================================


def test_record_frame():

    engine = ReplayEngine()

    engine.start()

    asset = create_asset()

    engine.record(
        step=1,
        assets=[asset],
    )

    assert engine.total_frames == 1


# ==========================================================
# Retrieve Frame
# ==========================================================


def test_get_frame():

    engine = ReplayEngine()

    engine.start()

    asset = create_asset()

    engine.record(
        step=1,
        assets=[asset],
    )

    frame = engine.frame(1)

    assert frame is not None

    assert frame.step == 1

    assert len(frame.assets) == 1


# ==========================================================
# Retrieve All Frames
# ==========================================================


def test_get_all_frames():

    engine = ReplayEngine()

    engine.start()

    asset = create_asset()

    for step in range(1, 6):

        engine.record(
            step=step,
            assets=[asset],
        )

    frames = engine.frames()

    assert len(frames) == 5


# ==========================================================
# Stop Recording
# ==========================================================


def test_replay_stop():

    engine = ReplayEngine()

    engine.start()

    engine.stop()

    assert engine.finished_at is not None


# ==========================================================
# Duration
# ==========================================================


def test_replay_duration():

    engine = ReplayEngine()

    engine.start()

    engine.stop()

    assert engine.duration >= 0


# ==========================================================
# Reset Replay
# ==========================================================


def test_replay_reset():

    engine = ReplayEngine()

    engine.start()

    asset = create_asset()

    engine.record(
        step=1,
        assets=[asset],
    )

    engine.reset()

    assert engine.total_frames == 0

    assert engine.started_at is None

    assert engine.finished_at is None


# ==========================================================
# Empty Replay
# ==========================================================


def test_empty_replay():

    engine = ReplayEngine()

    assert engine.total_frames == 0

    assert engine.frame(1) is None
