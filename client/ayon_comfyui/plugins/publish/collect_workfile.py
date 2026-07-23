import os

import pyblish.api


class CollectWorkfile(pyblish.api.InstancePlugin):
    """Collect current workflow path for publish.

    Note: This does not 'save' the current workfile and hence it may use
    an outdated state of the graph. It may make more sense to make this an
    extractor and serialize it on extraction instead.
    """

    order = pyblish.api.CollectorOrder - 0.49
    label = "Collect Workfile"
    hosts = ["comfyui"]
    families = ["workfile"]

    default_variant = "Main"

    def process(self, instance):

        current_workfile: str | None = instance.context.data["currentFile"]
        if current_workfile is None:
            self.log.warning(
                f"Can't collect current workfile because it's unsaved."
            )
            return

        staging_dir, filename = os.path.split(current_workfile)
        ext = os.path.splitext(filename)[1]

        # creating representation
        instance.data.setdefault("representations", []).append(
            {
                "name": ext[1:],
                "ext": ext[1:],
                "files": filename,
                "stagingDir": staging_dir,
            }
        )
