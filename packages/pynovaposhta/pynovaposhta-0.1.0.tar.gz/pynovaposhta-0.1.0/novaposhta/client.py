from typing import Optional

from .abstract import AbstractNovaposhta
from .models import (
    addresses, common, counterparties, internet_documents, scan_sheets
)


class Novaposhta(AbstractNovaposhta):
    def addresses(self, base_url: Optional[str] = None) -> addresses.Address:
        return addresses.Address(client=self, base_url=base_url)

    def common(self, base_url: Optional[str] = None):
        return common.Common(client=self, base_url=base_url)

    def counterparties(self, base_url: Optional[str] = None):
        return counterparties.Counterparty(client=self, base_url=base_url)

    def internet_documents(self, base_url: Optional[str] = None):
        return internet_documents.InternetDocument(
            client=self, base_url=base_url
        )

    @property
    def scan_sheets(self):
        return scan_sheets.ScanSheet(self)
