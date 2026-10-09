import csv
from collections import defaultdict
from pathlib import Path

from pydantic import ValidationError

from models import IllegallyParkedVehicle, NoiseComplaint, Pothole

DATA = Path(__file__).resolve().parent.parent / "data" / "ECC_Non-Emergency_Intake_Test_Set_40_Labeled_Chats.csv"

MODELS = {
    "noise_complaint": NoiseComplaint,
    "illegally_parked_vehicle": IllegallyParkedVehicle,
    "pothole": Pothole,
}


def load_chats(path: Path) -> dict[str, list[dict[str, str]]]:
    chats: dict[str, list[dict[str, str]]] = defaultdict(list)
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            chats[row["chat_id"]].append(row)
    return chats


def first_non_blank(rows: list[dict[str, str]], column: str) -> str | None:
    return next((r[column] for r in rows if r[column]), None)


def main() -> None:
    chats = load_chats(DATA)
    routine = {cid: rows for cid, rows in chats.items() if first_non_blank(rows, "chat_label") == "routine"}
    handoff = [cid for cid, rows in chats.items() if first_non_blank(rows, "chat_label") == "handoff"]
    print(f"chats routine: {len(routine)}, chats handoff: {len(handoff)}")

    valid, failures = 0, 0
    for cid, rows in routine.items():
        model = MODELS[first_non_blank(rows, "expected_request_type")]
        data = {field: first_non_blank(rows, f"expected_{field}") for field in model.model_fields}
        try:
            model(**data)
            valid += 1
        except ValidationError as e:
            failures += 1
            print(f"{cid} ({model.__name__}) failed:\n{e}")

    print(f"valid: {valid} of {len(routine)}")
    print("failures: none, 0 failures" if failures == 0 else f"failures: {failures}")


if __name__ == "__main__":
    main()
