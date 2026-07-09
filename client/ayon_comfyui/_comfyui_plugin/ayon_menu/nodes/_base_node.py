from __future__ import annotations

import hashlib
import json
from abc import abstractmethod

from comfy_api.latest import io


class AyonBaseNode(io.ComfyNode):

    node_id = "AYON Load Path"
    display_name = "AYON Load Path"
    category = "AYON"

    @classmethod  # pyright: ignore[reportArgumentType]
    def define_inputs(cls) -> list[io.Input]:
        pass

    @classmethod  # pyright: ignore[reportArgumentType]
    def define_outputs(cls) -> list[io.Output]:
        return []

    @classmethod
    def define_schema(cls):
        """Setup node definition."""
        return io.Schema(
            node_id=cls.node_id,
            display_name=cls.display_name,
            category=cls.category,
            inputs=cls.define_inputs(),
            outputs=cls.define_outputs(),
            is_output_node=True,
        )

    @classmethod
    def fingerprint_inputs(cls, **kwargs) -> str:
        """Generate a fingerprint of the inputs.

        Note:
            this is a very basic hash of the inputs.

        Args:
            kwargs: The inputs to the node.

        Returns:
            A fingerprint of the inputs.

        """
        data = json.dumps(kwargs, sort_keys=True)
        m = hashlib.sha256()
        m.update(data.encode('utf-8'))
        return m.digest().hex()

    @classmethod
    @abstractmethod
    def execute(cls, ayon_container_info: str, **kwargs) -> io.NodeOutput:  # ty:ignore[invalid-method-override]  # pyright: ignore[reportIncompatibleMethodOverride]
        raise NotImplementedError("Subclasses must implement this method")
