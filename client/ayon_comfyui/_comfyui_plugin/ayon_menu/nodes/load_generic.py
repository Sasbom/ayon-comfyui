from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
from comfy_api.latest import io

# IMPORT LOCAL LIBRARIES
from ._base_node import AyonBaseNode


class AyonLoadGenericNode(AyonBaseNode):
    """Container node loading a specified path."""

    node_id = "ayon.load.generic"
    display_name = "AYON Generic Loader"
    category = "AYON"

    @classmethod
    def define_inputs(cls):
        return [
            io.String.Input("project", "Project"),
            io.Combo.Input("folder_path", display_name="Folder Path", options=[]),
            io.Combo.Input("product", display_name="Product", options=[]),
            io.Combo.Input("version", display_name="Version", options=[]),
            io.Combo.Input("representation", display_name="Representation", options=[]),
            io.String.Input("representation_id", "Representation ID"),
            io.String.Input("filepath", "Filepath"),
        ]

    @classmethod
    def define_outputs(cls) -> list[io.Output]:
        return [
            io.String.Output(
                id="filepath",
                display_name="Filepath",
                tooltip="main filepath to the representation",
            ),
        ]

    @classmethod
    def validate_inputs(cls, **kwargs) -> bool | str:
        # the default validation fails because our combo options
        # are dynamically generated
        return True

    @classmethod
    async def execute(  # ty:ignore[invalid-method-override]  # pyright: ignore[reportIncompatibleMethodOverride]
        cls,
        filepath: str,
        **kwargs: typing.Any,
    ) -> io.NodeOutput:
        return io.NodeOutput(filepath)
