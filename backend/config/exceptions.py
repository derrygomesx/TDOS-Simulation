"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

exceptions.py

Custom exceptions used throughout TDOS.

Author  : TrackGuard AI Team
Version : 1.0.0
"""


# ==========================================================
# BASE EXCEPTION
# ==========================================================

class TDOSError(Exception):
    """
    Base exception for TDOS.
    """
    pass


# ==========================================================
# EXPERIMENTS
# ==========================================================

class ExperimentNotFoundError(TDOSError):
    """
    Raised when an experiment cannot be found.
    """
    pass


class ExperimentAlreadyExistsError(TDOSError):
    """
    Raised when an experiment already exists.
    """
    pass


# ==========================================================
# DATASETS
# ==========================================================

class DatasetNotFoundError(TDOSError):
    """
    Raised when a dataset does not exist.
    """
    pass


class DatasetUploadError(TDOSError):
    """
    Raised when dataset upload fails.
    """
    pass


# ==========================================================
# MODELS
# ==========================================================

class ModelNotFoundError(TDOSError):
    """
    Raised when a model cannot be found.
    """
    pass


class ModelRegistrationError(TDOSError):
    """
    Raised when model registration fails.
    """
    pass


# ==========================================================
# REPORTS
# ==========================================================

class ReportGenerationError(TDOSError):
    """
    Raised when report generation fails.
    """
    pass


# ==========================================================
# STORAGE
# ==========================================================

class StorageError(TDOSError):
    """
    Raised when storage operations fail.
    """
    pass


# ==========================================================
# SIMULATION
# ==========================================================

class SimulationError(TDOSError):
    """
    Raised when simulation API fails.
    """
    pass


# ==========================================================
# WEBSOCKET
# ==========================================================

class WebSocketError(TDOSError):
    """
    Raised when websocket communication fails.
    """
    pass


# ==========================================================
# AUTHENTICATION
# ==========================================================

class AuthenticationError(TDOSError):
    """
    Raised when authentication fails.
    """
    pass


class AuthorizationError(TDOSError):
    """
    Raised when authorization fails.
    """
    pass