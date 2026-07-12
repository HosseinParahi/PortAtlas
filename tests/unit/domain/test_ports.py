"""UT-DOM-001: port identity and state-vocabulary tests."""

from __future__ import annotations

import unittest

from portatlas.domain.ports import (
    AddressFamily,
    AssignmentState,
    BindScope,
    NamespaceKind,
    PortKey,
    PortNamespace,
    PortState,
    TransportProtocol,
)


class PortKeyTests(unittest.TestCase):
    def test_port_key_preserves_every_part_of_port_meaning(self) -> None:
        key = PortKey(
            protocol=TransportProtocol.TCP,
            port=4310,
            address_family=AddressFamily.IPV4,
            bind_address="127.0.0.1",
            namespace=PortNamespace.host(),
            host_identity="local",
        )

        self.assertEqual(key.bind_scope, BindScope.LOOPBACK)
        self.assertEqual(key.namespace.kind, NamespaceKind.HOST)
        self.assertEqual(key.port, 4310)

    def test_container_namespace_requires_an_opaque_adapter_identity(self) -> None:
        with self.assertRaises(ValueError):
            PortNamespace(kind=NamespaceKind.CONTAINER, identity=None)

        namespace = PortNamespace.container("container-ref-7")
        self.assertEqual(namespace.identity, "container-ref-7")

    def test_invalid_ports_and_bind_addresses_fail_closed(self) -> None:
        for port in (0, 65536):
            with self.subTest(port=port), self.assertRaises(ValueError):
                PortKey(protocol=TransportProtocol.TCP, port=port)

        with self.assertRaises(TypeError):
            PortKey(protocol=TransportProtocol.TCP, port=True)

        with self.assertRaises(ValueError):
            PortKey(
                protocol=TransportProtocol.UDP,
                port=53,
                bind_address="not an address",
                address_family=AddressFamily.IPV4,
            )

    def test_managed_and_unmanaged_state_vocabularies_do_not_collapse(self) -> None:
        self.assertIn(PortState.OBSERVED, PortState)
        self.assertIn(PortState.DECLARED, PortState)
        self.assertIn(AssignmentState.RESERVED, AssignmentState)
        self.assertIn(AssignmentState.LEASED, AssignmentState)
        self.assertNotEqual(PortState.OBSERVED.value, AssignmentState.RESERVED.value)


if __name__ == "__main__":
    unittest.main()
