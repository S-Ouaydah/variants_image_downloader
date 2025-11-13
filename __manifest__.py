{
    "name": "Variant Images Downloader",
    "summary": "Download all product variant images from the template form",
    'author': "Slomax",
    'category': 'Sales',
    'license': 'OPL-1',
    "Version": "0.2",
    "depends": ["base", "product", "sale"],
    'data': [
        "views/product_template_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'variants_image_download/static/src/js/download_multiple_images.js',
            ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
