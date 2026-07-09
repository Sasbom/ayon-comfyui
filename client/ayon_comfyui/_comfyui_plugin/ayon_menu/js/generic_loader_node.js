// @ts-check

import { app } from "../../../scripts/app.js";

import { get_ayon_extension } from "./ayon_menu.js";


const NODE_ID = "ayon.load.generic";

/*
    Utils
*/



/**
 * Find a widget by name
 * @param {any} node - The node to search in
 * @param {string} name - The name of the widget to find
 * @returns {any} - The widget
 */
function findWidget(node, name) {
    return node.widgets.find((w) => w.name === name)
}


/**
 * Call a client method
 * @param {string} method - The method to call
 * @param {object} params - The parameters to pass to the method
 * @returns {Promise<any>} - The result of the method call
 */
async function call_client_method(method, params) {
    const ext = get_ayon_extension();
    const result = await ext.IFRAMERPC.call("clientMethod", { method, params });
    return result;
}


/**
 * Get the folder paths for a project
 * @param {string} project_name - The name of the project
 * @returns {Promise<string[]>} - The folder paths
 */
async function get_folder_paths(project_name) {
    return await call_client_method(
        "ayonComfyUI.getFolders",
        {
            project_name: project_name,
        }
    );
}


/**
 * Get the product names for a project and folder path
 * @param {string} project_name - The name of the project
 * @param {string} folder_path - The path of the folder
 * @returns {Promise<string[]>} - The product names
 */
async function get_product_names(project_name, folder_path) {
    return await call_client_method(
    "ayonComfyUI.getProductNames",
    {
        project_name: project_name,
        folder_path: folder_path,
    });
}


/**
 * Get the versions for a project, folder path, and product name
 * @param {string} project_name - The name of the project
 * @param {string} folder_path - The path of the folder
 * @param {string} product_name - The name of the product
 * @returns {Promise<string[]>} - The versions
 */
async function get_versions(project_name, folder_path, product_name) {
    return await call_client_method(

    "ayonComfyUI.getVersions",
    {
        project_name: project_name,
        folder_path: folder_path,
        product_name: product_name,
    });
}


/**
 * Get the representations for a project, folder path, product name, and version
 * @param {string} project_name - The name of the project
 * @param {string} folder_path - The path of the folder
 * @param {string} product_name - The name of the product
 * @param {string} version - The version
 * @returns {Promise<string[]>} - The representations
 */
async function get_representations(project_name, folder_path, product_name, version) {
    return await call_client_method(
    "ayonComfyUI.getRepresentations",
    {
        project_name: project_name,
        folder_path: folder_path,
        product_name: product_name,
        version: version,
    });
}


/**
 * Get the representations for a project, folder path, product name, and version
 * @param {string} project_name - The name of the project
 * @param {string} folder_path - The path of the folder
 * @param {string} product_name - The name of the product
 * @param {string} version - The version
 * @returns {Promise<object>} - The representation
 */
async function get_representation(project_name, folder_path, product_name, version, representation_name) {
    return await call_client_method(
    "ayonComfyUI.getRepresentation",
    {
        project_name: project_name,
        folder_path: folder_path,
        product_name: product_name,
        version: version,
        representation_name: representation_name,
    });
}



/*
    Extension
*/

app.registerExtension({
    name: NODE_ID,

    beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== NODE_ID) return;

        const onCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = async function () {

            // apply original onNodeCreated
            onCreated?.apply(this, arguments);

            // get widgets
            const project_input = findWidget(this, "project");
            const folder_path_input = findWidget(this, "folder_path");
            const product_input = findWidget(this, "product");
            const version_input = findWidget(this, "version");
            const representation_input = findWidget(this, "representation");
            const representation_id_input = findWidget(this, "representation_id");
            const filepath_input = findWidget(this, "filepath");

            /*
            Event handlers
            */
            async function updateFolderPaths() {
                folder_path_input.options.values = await get_folder_paths(
                    project_input.value,
                );
            }

            async function updateProductNames() {
                product_input.options.values = await get_product_names(
                    project_input.value,
                    folder_path_input.value,
                );
            }

            async function updateVersions() {
                version_input.options.values = await get_versions(
                    project_input.value,
                    folder_path_input.value,
                    product_input.value,
                );
            }

            async function updateRepresentations() {
                representation_input.options.values = await get_representations(
                    project_input.value,
                    folder_path_input.value,
                    product_input.value,
                    version_input.value,
                );
            }

            async function updateRepresentation() {
                const representation = await get_representation(
                    project_input.value,
                    folder_path_input.value,
                    product_input.value,
                    version_input.value,
                    representation_input.value,
                );
                representation_id_input.value = representation?.id || "not found";
                filepath_input.value = representation?.path || "not found";
            }

            project_input.callback = async () => {
                await updateFolderPaths();
                await updateProductNames();
                await updateVersions();
                await updateRepresentations();
                await updateRepresentation();
            }

            folder_path_input.callback = async () => {
                await updateProductNames();
                await updateVersions();
                await updateRepresentations();
                await updateRepresentation();
            }

            product_input.callback = async () => {
                await updateVersions();
                await updateRepresentations();
                await updateRepresentation();
            }

            version_input.callback = async () => {
                await updateRepresentations();
                await updateRepresentation();
            }

            representation_input.callback = async () => {
                await updateRepresentation();
            }

            async function updateAll() {
                await updateFolderPaths();
                await updateProductNames();
                await updateVersions();
                await updateRepresentations();
                await updateRepresentation();
            }

            await updateAll();

            const refresh_button = this.addWidget(
                "button",
                "refresh",
                "",
                async () => updateAll()
            );
        };

        /**
         * runs once after the graph is configured
         */
        nodeType.prototype.onGraphConfigured = async function () {
            const widgets_to_update = [
                "project",
                "folder_path",
                "product",
                "version",
            ]

            for (const widget_name of widgets_to_update) {
                const widget = findWidget(this, widget_name);
                await widget?.callback?.();
            }
        };

    },
});
