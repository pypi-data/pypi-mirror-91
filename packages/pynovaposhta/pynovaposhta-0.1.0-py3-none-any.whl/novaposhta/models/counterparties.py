from typing import Optional, List

import httpx

from novaposhta.schemas.counterparties import (
    CounterpartyAddress, CounterpartyOptions, CounterpartyContactPerson,
    Counterparty as CounterpartySchema, ContactPerson as ContactPersonSchema, NewCounterparty, DeleteResponse
)
from .abstract import AbstractClient

__all__ = (
    'Counterparty',
    # 'AsyncCounterparty'
)


class Counterparty(AbstractClient):
    MODEL = 'Counterparty'

    def get_addresses(self, ref: str, counterparty_property: str = 'sender'):
        request = self.build_request(
            url=self.build_url('getCounterpartyAddresses'),
            json=self.build_params(
                'getCounterpartyAddresses',
                {'Ref': ref, 'CounterpartyProperty': counterparty_property}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CounterpartyAddress)

    def get_options(self, ref: str):
        request = self.build_request(
            url=self.build_url('getCounterpartyOptions'),
            json=self.build_params(
                'getCounterpartyOptions',
                {'Ref': ref}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CounterpartyOptions)

    def get_contact_persons(self, ref: str, page: int = 1):
        request = self.build_request(
            url=self.build_url('getCounterpartyContactPersons'),
            json=self.build_params(
                'getCounterpartyContactPersons',
                {'Ref': ref, 'Page': page}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CounterpartyContactPerson)

    def list(
        self,
        counterparty_property: str = 'Sender',
        find_by_string: str = None,
        page: int = 1
    ) -> List[CounterpartySchema]:
        request = self.build_request(
            url=self.build_url('getCounterparties'),
            json=self.build_params(
                'getCounterparties',
                {
                    'CounterpartyProperty': counterparty_property,
                    'FindByString': find_by_string,
                    'Page': page
                }
            ),
            headers=self.get_headers()
        )
        response = self.make_request(request)

        return self.process_response(response, model=CounterpartySchema)

    def update(
        self,
        ref: str,
        city_ref: str,
        first_name: str,
        last_name: str,
        phone: str,
        email: str,
        counterparty_type: str,
        counterparty_property: str,
        middle_name: Optional[str] = None,
    ):
        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update',
                {
                    "CityRef": city_ref,
                    "Ref": ref,
                    "FirstName": first_name,
                    "LastName": last_name,
                    "MiddleName": middle_name,
                    "Phone": phone,
                    "Email": email,
                    "CounterpartyType": counterparty_type,
                    "CounterpartyProperty": counterparty_property,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CounterpartySchema)

    def update_personal(self, ref: str, phone: str):
        """
        Частные лица могут изменять только телефон
        :param ref:
        :param phone:
        :return:
        """

        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update',
                {
                    "Ref": ref,
                    "Phone": phone,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=CounterpartySchema)

    def save(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        phone: str,
        email: str,
        counterparty_type: str,
        counterparty_property: str,
    ):

        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update',
                {
                    "FirstName": first_name,
                    "MiddleName": middle_name,
                    "LastName": last_name,
                    "Phone": phone,
                    "Email": email,
                    "CounterpartyType": counterparty_type,
                    "CounterpartyProperty": counterparty_property,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=NewCounterparty)

    def save_legal_entity(
        self,
        counterparty_type: str,
        counterparty_property: str,
        edrpou: str,
    ):

        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update',
                {
                    "CounterpartyType": counterparty_type,
                    "EDRPOU": edrpou,
                    "CounterpartyProperty": counterparty_property,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=NewCounterparty)

    def save_thirdparty(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        phone: str,
        email: str,
        counterparty_type: str,
        counterparty_property: str,
        edrpou: int,
        ownership_form: str
    ):
        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update',
                {
                    "FirstName": first_name,
                    "MiddleName": middle_name,
                    "LastName": last_name,
                    "Phone": phone,
                    "Email": email,
                    "CounterpartyType": counterparty_type,
                    "CounterpartyProperty": counterparty_property,
                    "EDRPOU": edrpou,
                    "OwnershipForm": ownership_form
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=NewCounterparty)

    def delete(self, ref: str):
        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {"Ref": ref}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeleteResponse)


class ContactPerson(AbstractClient):
    MODEL = 'ContactPerson'

    def update(
        self,
        counterparty_ref: str,
        ref: str,
        first_name: str,
        last_name: str,
        middle_name: str,
        phone: str,
    ):
        request = self.build_request(
            url=self.build_url('update'),
            json=self.build_params(
                'update',
                {
                    "CounterpartyRef": counterparty_ref,
                    "Ref": ref,
                    "FirstName": first_name,
                    "LastName": last_name,
                    "MiddleName": middle_name,
                    "Phone": phone,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ContactPersonSchema)

    def save(
        self,
        counterparty_ref: str,
        first_name: str,
        last_name: str,
        middle_name: str,
        phone: str,
    ):
        request = self.build_request(
            url=self.build_url('save'),
            json=self.build_params(
                'save',
                {
                    "CounterpartyRef": counterparty_ref,
                    "FirstName": first_name,
                    "LastName": last_name,
                    "MiddleName": middle_name,
                    "Phone": phone,
                }
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=ContactPersonSchema)

    def delete(self, ref: str):
        request = self.build_request(
            url=self.build_url('delete'),
            json=self.build_params(
                'delete',
                {"Ref": ref}
            ),
            headers=self.get_headers()
        )

        response = httpx.Client().send(request)

        return self.process_response(response, model=DeleteResponse)
