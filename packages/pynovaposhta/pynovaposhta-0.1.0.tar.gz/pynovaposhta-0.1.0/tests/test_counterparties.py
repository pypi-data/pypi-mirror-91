from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from novaposhta.client import Novaposhta


def test_counterparties_list(client: 'Novaposhta'):
    counterparties = client.counterparties().list()
    assert len(counterparties) == 1
