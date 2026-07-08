# IMPORT THIRD PARTY LIBRARIES
import ayon_api


def get_representation_by_names(
    project_name: str,
    folder_path: str,
    product_name: str,
    version_name: int | str,
    representation_name: str,
) -> dict | None:
    """Get representation entity for folder and product.

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
