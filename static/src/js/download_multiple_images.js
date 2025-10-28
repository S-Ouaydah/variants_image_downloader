/** @odoo-module **/

import { registry } from "@web/core/registry";

function downloadMultipleImages(env, action) {
    const images = action.params.images || [];
    const total = action.params.total || images.length;

    if (images.length === 0) {
        env.services.notification.add("No images to download", { type: "warning" });
        return;
    }

    env.services.notification.add(
        `Downloading ${total} images... Please wait.`,
        { type: "info" }
    );

    // Download each image with delay
    images.forEach((image, index) => {
        setTimeout(() => {
            downloadImage(image.url, image.name);

            // Show progress notification
            if (index === images.length - 1) {
                env.services.notification.add(
                    `Successfully downloaded ${total} images!`,
                    { type: "success" }
                );
            }
        }, index * 600); // 600ms delay between downloads
    });
}

function downloadImage(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();

    // Cleanup
    setTimeout(() => {
        document.body.removeChild(link);
    }, 100);
}

registry.category("actions").add("download_multiple_images", downloadMultipleImages);