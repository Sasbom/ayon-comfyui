from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import json
import typing

# IMPORT THIRD PARTY LIBRARIES
from comfy_api.latest import io, ui

# IMPORT LOCAL LIBRARIES
from ._base_node import AyonBaseNode
from ..lib import get_representation_by_names, fill_roots


class AyonLoadGenericNode(AyonBaseNode):
    """Container node loading a specified path."""

    node_id = "ayon.load.generic"
    display_name = "AYON Generic Loader"
    category = "AYON"

    @classmethod
    def define_inputs(cls) -> list[io.Input]:

        return [
            io.String.Input("project", "Project"),
            io.String.Input("folder_path", "Folder Path"),
            io.String.Input("product", "Product"),
            io.String.Input("version", "Version"),
            io.String.Input("representation", "Representation"),

            # TODO: make this read only
            # io.String.Input(
            #     "representation_id",
            #     "Representation ID",
            #     socketless=True,
            #     optional=True,
            # ),  # noqa: E501
        ]

    @classmethod
    def define_outputs(cls) -> list[io.Output]:
        return [
            io.String.Output(
                id="filepath",
                display_name="Filepath",
                tooltip="main filepath to the representation",
            ),
            io.String.Output(
                id="files",
                display_name="Files",
                tooltip="List of files in the representation",
                is_output_list=True,
            ),
        ]

    @classmethod
    def execute(  # ty:ignore[invalid-method-override]  # pyright: ignore[reportIncompatibleMethodOverride]
        cls,
        project: str,
        folder_path: str,
        product: str,
        version: str,
        representation: str,
        **kwargs: typing.Any,
    ) -> io.NodeOutput:
        representation_entity = get_representation_by_names(
            project,
            folder_path,
            product,
            version,
            representation,
        )
        if not representation_entity:
            raise ValueError(f"Representation {representation} not found")

        attrib = representation_entity.get("allAttrib", {})
        if isinstance(attrib, str):
            attrib = json.loads(attrib)

        path = attrib.get("path", "")
        path = fill_roots(path)

        files = representation_entity.get("files", [])
        paths = []
        for file in files:
            path = file.get("path", "")
            path = fill_roots(path)
            paths.append(path)

        representation_id = representation_entity.get("id", "")

        return io.NodeOutput(
            path,
            paths,
            ui=ui.PreviewText(representation_id)
        )
