# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Nota de Pedido Export",
    "summary": "Exportar productos a CSV para Nota de Pedido",
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "17.0.10.6.1",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "stock",
        "account",
        "product_replenishment_cost",
        "pricelist_replenishment_cost",
    ],
    "data": [
        "views/product_views.xml",
        "views/export_ndp_wizard_views.xml",
        "security/ir.model.access.csv",
    ],
}
