# wizards/export_ndp_wizard.py
from odoo import models, fields
import csv
import io
import base64


class ExportNDPWizard(models.TransientModel):
    _name = "export.ndp.wizard"

    product_ids = fields.Many2many("product.product", string="Productos a Exportar")
    datas = fields.Binary(string="CSV Data", attachment=True)

    def generate_csv(self):
        uom_mapping = {
            "Unidades": "UN",
            "Unidad": "UNI",
        }
        for product in self.product_ids:
            product._compute_cotizacion_dolar()
            product._compute_nombre_producto()
            product._compute_precios()
            product._compute_precios_pesos()
            product._compute_stock()
        output = io.StringIO()
        writer = csv.writer(output, delimiter="|")
        for product in self.product_ids:
            unidad_medida = (
                uom_mapping.get(product.ndp_unidad_medida, product.ndp_unidad_medida)
                or ""
            )
            codigo_barra = (
                product.ndp_codigo_barra
                if product.ndp_codigo_barra and product.ndp_codigo_barra != "0"
                else ""
            )
            if product.ndp_moneda == "DO" and product.ndp_cotizacion_dolar is not None:
                ndp_cotizacion_dolar_exportar = product.ndp_cotizacion_dolar
            else product.ndp_moneda == "PE":
                ndp_cotizacion_dolar_exportar = 1

            # Formatear la fecha como DD/MM/YY
            fecha_cambio_costo = (
                product.ndp_ultimo_cambio_costo.strftime("%d/%m/%y")
                if product.ndp_ultimo_cambio_costo
                else ""
            )
            writer.writerow(
                [
                    product.ndp_rubro or "",
                    product.ndp_nombre_rubro or "",
                    product.ndp_sku or "",
                    product.ndp_nombre_producto or "",
                    product.ndp_familia or "",
                    product.ndp_codigo_area or "",
                    product.ndp_nombre_area or "",
                    f"{product.ndp_precio_publico_moneda:.3f}",
                    f"{product.ndp_precio_mayorista_moneda:.3f}",
                    f"{product.ndp_iva_porcentaje:.0f}",
                    unidad_medida,
                    product.ndp_nombre_foto or "",
                    codigo_barra,
                    product.ndp_moneda or "",
                    f"{product.ndp_precio_publico_pesos:.3f}",
                    f"{product.ndp_precio_mayorista_pesos:.3f}",
                    f"{ndp_cotizacion_dolar_exportar:.3f}"
                    f"{product.ndp_stock:.0f}",
                    f"{product.ndp_costo:.3f}",
                    f"{product.ndp_pto_pedido:.3f}",
                    product.ndp_url_web or "",
                    product.ndp_ultimo_cambio_costo or "",
                    product.ndp_observaciones or "",
                    "",
                ]
            )
        data = output.getvalue().encode("utf-8")
        self.datas = base64.b64encode(data)
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/?model=%s&id=%s&field=datas&download=true&filename=ndp_export.csv"
            % (self._name, self.id),
            "target": "self",
        }
