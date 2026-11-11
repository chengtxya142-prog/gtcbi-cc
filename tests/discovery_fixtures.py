"""Fresh fictional records for discovery contract tests."""


def discovery_fixture():
    return {
        "model_version": "2.0.2",
        "discovery_schema": "discovery-gate-v1",
        "synthetic": True,
        "discovery_id": "SYN-DISC-001",
        "entry_mode": "discovery",
        "snapshot": {
            "revision": "P1",
            "company": "Synthetic Seller (fictional)",
            "industry": "workwear",
            "products": ["workwear"],
            "markets": ["GB"],
            "customer_types": ["distributor"],
            "cooperation_objective": "supply",
            "keywords": {
                "include": ["workwear distributor"],
                "exclude": [],
                "provenance": ["operator"],
            },
            "profile_confirmation": {
                "confirmed": True, "revision": "P1",
                "basis": "Synthetic profile approval", "confirmed_at": None,
            },
            "keyword_confirmation": {
                "confirmed": True, "revision": "P1",
                "basis": "Synthetic keyword approval", "confirmed_at": None,
            },
        },
        "batches": [{
            "id": "B1", "kind": "initial",
            "requested_count": 10, "quantity_basis": "default",
            "actual_count": 1, "candidate_ids": ["CAND-001"],
            "snapshot_revision": "P1",
            "shortfall_reason": "Synthetic bounded-source exercise",
        }],
        "candidates": [{
            "id": "CAND-001", "name": "Example Workwear (fictional)",
            "country": "GB", "website": "https://buyer.example.invalid",
            "match_reason": "Synthetic product-channel relevance, not a conclusion",
            "sources": [{
                "url": "https://buyer.example.invalid/about",
                "access_state": "read", "checked_on": "2026-11-10",
            }],
            "entity_key": "SYN-BUYER-GB", "status": "pending",
            "snapshot_revision": "P1",
        }],
        "selection": [], "approval": None,
        "approval_history": [], "runs": [],
    }


def approve(data, ids=None):
    chosen = ["CAND-001"] if ids is None else list(ids)
    data["selection"] = chosen
    data["approval"] = {
        "id": "SYN-APPROVAL-001", "candidate_ids": list(chosen),
        "snapshot_revision": "P1", "confirmed": True,
        "basis": "Synthetic operator selection and start confirmation",
        "confirmed_at": None,
    }
    for candidate in data["candidates"]:
        if candidate["id"] in chosen:
            candidate["status"] = "selected"
    return data
