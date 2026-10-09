from pydantic import BaseModel


class NoiseComplaint(BaseModel):
    location: str
    noise_source: str
    callback_phone: str


class IllegallyParkedVehicle(BaseModel):
    location: str
    vehicle_description: str
    license_plate: str | None  # blank in ECC-T-010, ECC-T-025, ECC-T-037 (plate unreadable)
    blocking_driveway: bool
    callback_phone: str


class Pothole(BaseModel):
    location: str
    pothole_size: str
    hazard_to_traffic: bool
    callback_phone: str
