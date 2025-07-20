from odoo import models, fields, api
import csv
import io
import base64


class ExportNDPWizard(models.TransientModel):
    _name = "export.ndp.wizard"

    product_ids = fields.Many2many("product.template", string="Productos a Exportar")
    datas = fields.Binary(
        string="CSV Data", attachment=True
    )  # Campo temporal para el CSV

    def generate_csv(self):
        # Mapeo de unidades de medida de Odoo a códigos NDP
        uom_mapping = {
            "Unidades": "UN",
            "Unidad": "UN",
            # Agrega más mapeos si hay otras unidades en el sistema
        }

        # Forzar recomputo de todos los campos computados
        self.product_ids.invalidate_cache(
            fnames=[
                "ndp_nombre_producto",
                "ndp_precio_publico_moneda",
                "ndp_precio_mayorista_moneda",
                "ndp_iva_porcentaje",
                "ndp_cotizacion_dolar",
                "ndp_precio_publico_pesos",
                "ndp_precio_mayorista_pesos",
                "ndp_stock",
            ],
            ids=self.product_ids.ids,
        )

        output = io.StringIO()
        writer = csv.writer(output, delimiter="|")
        for product in self.product_ids:
            # Mapear unidad de medida
            unidad_medida = (
                uom_mapping.get(product.ndp_unidad_medida, product.ndp_unidad_medida)
                or ""
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
                    f"{product.ndp_iva_porcentaje:.1f}",
                    unidad_medida,
                    product.ndp_nombre_foto or "",
                    product.ndp_codigo_barra or "",
                    product.ndp_moneda or "",
                    f"{product.ndp_precio_publico_pesos:.3f}",
                    f"{product.ndp_precio_mayorista_pesos:.3f}",
                    f"{product.ndp_cotizacion_dolar:.3f}",
                    f"{product.ndp_stock:.3f}",
                    f"{product.ndp_costo:.3f}",
                    f"{product.ndp_pto_pedido:.3f}",
                    product.ndp_url_web or "",
                    product.ndp_ultimo_cambio_costo or "",
                    product.ndp_observaciones or "",
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
