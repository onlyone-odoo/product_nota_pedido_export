# wizards/export_ndp_wizard.py
from odoo import models, fields
import csv
import io
import base64  # Agrega este import


class ExportNDPWizard(models.TransientModel):
    _name = "export.ndp.wizard"

    product_ids = fields.Many2many("product.template", string="Productos a Exportar")
    datas = fields.Binary(
        string="CSV Data", attachment=True
    )  # Campo temporal para el CSV

    def generate_csv(self):
        output = io.StringIO()
        writer = csv.writer(output, delimiter="|")
        for product in self.product_ids:
            writer.writerow(
                [
                    product.ndp_rubro or "",
                    product.ndp_nombre_rubro or "",
                    product.ndp_sku or "",
                    product.ndp_nombre_producto or "",
                    product.ndp_familia or "",
                    product.ndp_codigo_area or "",
                    product.ndp_nombre_area or "",
                    product.ndp_precio_publico_moneda,
                    product.ndp_precio_mayorista_moneda,
                    product.ndp_iva_porcentaje,
                    product.ndp_unidad_medida or "",
                    product.ndp_nombre_foto or "",
                    product.ndp_codigo_barra or "",
                    product.ndp_moneda or "",
                    product.ndp_precio_publico_pesos,
                    product.ndp_precio_mayorista_pesos,
                    product.ndp_cotizacion_dolar,
                    product.ndp_stock,
                    product.ndp_costo,
                    product.ndp_pto_pedido,
                    product.ndp_url_web or "",
                    product.ndp_ultimo_cambio_costo or "",
                    product.ndp_observaciones or "",
                ]
            )
        data = output.getvalue().encode("utf-8")
        self.datas = base64.b64encode(data)  # Encode y guarda en el campo Binary
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/?model=%s&id=%s&field=datas&download=true&filename=ndp_export.csv"
            % (self._name, self.id),
            "target": "self",
        }
