from odoo import models, api
import json


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def download_variant_images(self):
        """Trigger download of all variant images individually"""
        variants = self.product_variant_ids.filtered(lambda v: v.image_1920)

        if not variants:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'No variant images found',
                    'type': 'warning',
                }
            }

        # Prepare image data for JavaScript
        images = []
        for variant in variants:
            # Create temporary attachment for download
            attachment = self.env['ir.attachment'].create({
                'name': f"{variant.default_code or variant.id}_{variant.name}.png",
                'type': 'binary',
                'datas': variant.image_1920,
                'mimetype': 'image/png',
                'res_model': 'product.product',
                'res_id': variant.id,
                'public': True,  # Temporary public access
            })

            images.append({
                'id': attachment.id,
                'name': attachment.name,
                'url': f'/web/content/{attachment.id}?download=true'
            })

        # Return client action to trigger downloads
        return {
            'type': 'ir.actions.client',
            'tag': 'download_multiple_images',
            'params': {
                'images': images,
                'total': len(images)
            }
        }
