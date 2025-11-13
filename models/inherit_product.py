from odoo import models
import hashlib


class ProductVariant(models.Model):
    _inherit = 'product.product'

    def download_variant_images(self):
        """Trigger download of this variant's image"""
        if not self.image_1920:
            return
        # Search for existing attachment for this product's image
        attachment = self.env['ir.attachment'].search([
            ('res_model', '=', 'product.product'),
            ('res_id', '=', self.id),
            ('res_field', '=', 'image_1920'),
        ], limit=1)

        # If no attachment exists, create one
        if not attachment:
            attachment = self.env['ir.attachment'].create({
                'name': f"{self.default_code or self.id}_{self.name}.png",
                'type': 'binary',
                'datas': self.image_1920,
                'mimetype': 'image/png',
                'res_model': 'product.product',
                'res_id': self.id,
                'res_field': 'image_1920',
                'public': True,
            })

        # Return client action to trigger download
        return {
            'type': 'ir.actions.client',
            'tag': 'download_image',
            'params': {
                'image': {
                    'id': attachment.id,
                    'name': attachment.name or f"{self.default_code or self.id}_{self.name}.png",
                    'url': f'/web/content/{attachment.id}?download=true'
                }
            }
        }


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def download_variant_images(self):
        """Trigger download of unique variant images only"""
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

        # Track unique images by hash
        unique_images = {}
        images = []

        for variant in variants:
            # Create hash of image data to detect duplicates
            image_hash = hashlib.md5(variant.image_1920).hexdigest()

            # Skip if we've already seen this image
            if image_hash in unique_images:
                continue

            # Mark this hash as seen
            unique_images[image_hash] = True

            # Search for existing attachment for this variant's image
            attachment = self.env['ir.attachment'].search([
                ('res_model', '=', 'product.product'),
                ('res_id', '=', variant.id),
                ('res_field', '=', 'image_1920'),
            ], limit=1)

            # If no attachment exists, create one
            if not attachment:
                attachment = self.env['ir.attachment'].create({
                    'name': f"{variant.default_code or variant.id}_{variant.name}.png",
                    'type': 'binary',
                    'datas': variant.image_1920,
                    'mimetype': 'image/png',
                    'res_model': 'product.product',
                    'res_id': variant.id,
                    'res_field': 'image_1920',
                    'public': True,
                })

            images.append({
                'id': attachment.id,
                'name': attachment.name or f"{variant.default_code or variant.id}_{variant.name}.png",
                'url': f'/web/content/{attachment.id}?download=true'
            })

        if not images:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'All variant images are duplicates',
                    'type': 'warning',
                }
            }

        # Return client action to trigger downloads
        return {
            'type': 'ir.actions.client',
            'tag': 'download_multiple_images',
            'params': {
                'images': images,
                'total': len(images),
                'skipped': len(variants) - len(images)
            }
        }