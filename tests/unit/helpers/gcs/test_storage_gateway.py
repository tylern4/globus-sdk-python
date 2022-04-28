import pytest

from globus_sdk import (
    POSIXStagingStoragePolicies,
    POSIXStoragePolicies,
    StorageGatewayDocument,
)


@pytest.mark.parametrize(
    "use_kwargs,doc_version",
    [
        ({}, "1.0.0"),
        ({"require_mfa": True}, "1.1.0"),
        ({"require_mfa": False}, "1.1.0"),
    ],
)
def test_datatype_version_deduction(use_kwargs, doc_version):
    sg = StorageGatewayDocument(**use_kwargs)
    assert sg["DATA_TYPE"] == f"storage_gateway#{doc_version}"


def test_storage_gateway_policy_document_conversion():
    policies = POSIXStoragePolicies(
        groups_allow=["jedi", "wookies"], groups_deny=["sith", "stormtroopers"]
    )
    sg = StorageGatewayDocument(policies=policies)
    assert "policies" in sg
    assert isinstance(sg["policies"], dict)
    assert sg["policies"] == {
        "DATA_TYPE": "posix_storage_policies#1.0.0",
        "groups_allow": ["jedi", "wookies"],
        "groups_deny": ["sith", "stormtroopers"],
    }


def test_posix_staging_env_vars():
    p = POSIXStagingStoragePolicies(
        groups_allow=("vulcans", "starfleet"),
        groups_deny=(x for x in ("ferengi", "romulans")),
        stage_app="/globus/bin/posix-stage-data",
        environment=({"name": "VOLUME", "value": "/vol/0"},),
    )

    assert isinstance(p["environment"], list)
    assert dict(p) == {
        "DATA_TYPE": "posix_staging_storage_policies#1.0.0",
        "groups_allow": ["vulcans", "starfleet"],
        "groups_deny": ["ferengi", "romulans"],
        "stage_app": "/globus/bin/posix-stage-data",
        "environment": [{"name": "VOLUME", "value": "/vol/0"}],
    }
