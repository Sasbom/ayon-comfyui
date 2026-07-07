from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import json
import typing

# IMPORT THIRD PARTY LIBRARIES
from comfy_api.latest import io, ui
import ayon_api

# IMPORT LOCAL LIBRARIES
from ._base_node import AyonBaseNode


def get_representation_by_names(
    project_name: str,
    folder_path: str,
    product_name: str,
    version_name: int | str,
    representation_name: str,
) -> dict | None:
    """Get representation entity for folder and product.

    TODO:
        move this into lib

    Args:
        project_name: The name of the project.
        folder_path: The path of the folder.
        product_name: The name of the product.
        version_name: The name of the version.
            can be an integer or a string.
            string can be either a version number, with optional "v" prefix.
            or on of the following strings: "hero", "latest".
        representation_name: The name of the representation.

    Returns:
        representation_entity: The representation entity or None if not found.

    """
    folder_entity = ayon_api.get_folder_by_path(
        project_name,
        folder_path,
        fields=["id"],
    )
    if not folder_entity:
        return None

    product_entity = ayon_api.get_product_by_name(
        project_name,
        product_name,
        folder_id=folder_entity["id"],
        fields=["id"],
    )
    if not product_entity:
        return None

    if version_name == "hero":
        version_entity = ayon_api.get_hero_version_by_product_id(
            project_name,
            product_id=product_entity["id"],
        )
    elif version_name == "latest":
        version_entity = ayon_api.get_last_version_by_product_id(
            project_name,
            product_id=product_entity["id"],
        )
    else:
        if isinstance(version_name, str):
            version_name = version_name.lstrip("v")
            version = int(version_name)
        else:
            version = version_name

        version_entity = ayon_api.get_version_by_name(
            project_name,
            version=version,
            product_id=product_entity["id"],
        )
    if not version_entity:
        return None

    return ayon_api.get_representation_by_name(
        project_name,
        representation_name,
        version_id=version_entity["id"],
    )


def fill_roots(path: str) -> str:
    """Fill the roots in the path.

    TODO:
        implement this

    Args:
        path: The path to fill the roots in.

    Returns:
        The path with the roots filled.
    """
    return path.replace("{root[work]}", "/mnt/jobs")


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
