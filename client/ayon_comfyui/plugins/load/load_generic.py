"""Load image definition."""

from __future__ import annotations

from ayon_comfyui.api.plugin import ComfyUILoader


class GenericLoader(ComfyUILoader):
    """Load generic representation."""

    product_types = {"*"}
    representations = {"*"}
    extensions = {"*"}

    label = "Generic Loader"
    icon = "link"
    order = 10
    color = "orange"

    def load(
        self,
        context: dict,
        name: str | None = None,
        namespace: str | None = None,
        options: dict | None = None,
    ) -> None:
        """Load asset via database.

        Arguments:
            context (dict): Full parenthood of representation to load
            name (str, optional): Use pre-defined name
            namespace (str, optional): Use pre-defined namespace
            options (dict, optional): Additional settings dictionary

        """
        project = context.get("project") or {}
        folder = context.get("folder") or {}
        product = context.get("product") or {}
        version = context.get("version") or {}
        representation = context.get("representation") or {}

        # Create the generic loader node.
        parms = {
            "project": project.get("name", ""),
            "folder_path": folder["path"],
            "product": product.get("name", ""),
            "version": version.get("version", ""),
            "representation": representation.get("name", ""),
            "representation_id": representation.get("id", ""),
        }

        self.stub.create_node(node_type="ayon.load.generic", parms=parms)

    def remove(self, container: dict) -> None:
        """Remove container from context and scene."""
        self.stub.remove_containers(container)
        self.stub.remove_load_nodes(container)

    def update(self, container: dict, context: dict) -> None:
        """Update container with new uploaded file."""
        raise NotImplementedError("Not implemented")

    def switch(self, container: dict, context: dict) -> None:
        """Provide interface for switching calls."""
        self.update(container=container, context=context)
