import csv
import io
import base64
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Campos personalizados para "DATOS NOTA DE PEDIDO"
    np_rubro = fields.Integer(string="Rubro")
    np_nombre_rubro = fields.Char(string="Nombre del Rubro")
    np_familia = fields.Char(string="Familia")
    np_codigo_area = fields.Integer(string="Código de Área")
    np_nombre_area = fields.Char(string="Nombre del Área")
    np_precio_publico_moneda = fields.Float(string="Precio Público según Moneda")
    np_precio_mayorista_moneda = fields.Float(string="Precio Mayorista según Moneda")
    np_porcentaje_iva = fields.Float(
        string="% de IVA", default=21.0
    )  # Ej. 21% por defecto
    np_unidad_medida = fields.Char(string="Unidad de Medida", default="UN")
    np_nombre_foto = fields.Char(string="Nombre Archivo de Foto")
    np_codigo_barra = fields.Char(
        string="Código de Barra"
    )  # Usa barcode si prefieres el estándar
    np_moneda = fields.Char(string="Moneda", default="DO")  # Ej. 'DO' para dólar
    np_precio_publico_dolar = fields.Float(
        string="Precio Público $", compute="_compute_precios_dolar", store=True
    )
    np_precio_mayorista_dolar = fields.Float(
        string="Precio Mayorista $", compute="_compute_precios_dolar", store=True
    )
    np_cotizacion = fields.Float(
        string="Cotización", default=1280.0
    )  # Ej. cotización fija, ajusta a un campo global si necesitas
    np_costo = fields.Float(
        string="Costo", related="standard_price"
    )  # Relacionado con costo estándar
    np_pto_pedido = fields.Float(string="Pto Pedido")
    np_url_web = fields.Char(string="URL Web")
    np_ultimo_cambio_costo = fields.Date(string="Último Cambio Costo")
    np_observaciones = fields.Text(string="Observaciones")

    @api.depends(
        "np_precio_publico_moneda",
        "np_precio_mayorista_moneda",
        "np_cotizacion",
        "np_moneda",
    )
    def _compute_precios_dolar(self):
        for product in self:
            if product.np_moneda == "DO":  # Si ya en dólar, multiplica por cotización
                product.np_precio_publico_dolar = (
                    product.np_precio_publico_moneda * product.np_cotizacion
                )
                product.np_precio_mayorista_dolar = (
                    product.np_precio_mayorista_moneda * product.np_cotizacion
                )
            else:  # Asume conversión simple; ajusta lógica real
                product.np_precio_publico_dolar = product.np_precio_publico_moneda
                product.np_precio_mayorista_dolar = product.np_precio_mayorista_moneda

    def export_products_to_csv(self):
        output = io.StringIO()
        writer = csv.writer(
            output,
            delimiter="|",
            lineterminator="\n",
            quoting=csv.QUOTE_NONE,
            escapechar="\\",
        )

        # Obtener productos (filtra según necesidad, ej. solo activos)
        products = self.search(
            [("detailed_type", "=", "product")]
        )  # Ej. solo storables

        for product in products:
            row = [
                product.np_rubro or "",  # 1 rubro
                product.np_nombre_rubro or "",  # 2 nombre del rubro
                product.default_code or "",  # 3 sku
                product.name or "",  # 4 nombre producto
                product.np_familia or "",  # 5 FAMILIA
                product.np_codigo_area or "",  # 6 codigo de Area
                product.np_nombre_area or "",  # 7 nombre del Area
                product.np_precio_publico_moneda or "",  # 8 precio publico segun moneda
                product.np_precio_mayorista_moneda or "",  # 9 precio mayorista
                product.np_porcentaje_iva or "",  # 10 % de IVA
                product.np_unidad_medida or "",  # 11 unidad de medida
                product.np_nombre_foto or "",  # 12 nombre archivo de foto
                product.np_codigo_barra or "",  # 13 codigo barra
                product.np_moneda or "",  # 14 MONEDA
                product.np_precio_publico_dolar or "",  # 15 precio publico $
                product.np_precio_mayorista_dolar or "",  # 16 precio mayorista $
                product.np_cotizacion or "",  # 17 COTIZACION
                product.qty_available or "",  # 18 STOCK (stock disponible)
                product.np_costo or "",  # 19 costo
                product.np_pto_pedido or "",  # 20 pto pedido
                product.np_url_web or "",  # 21 url web
                product.np_ultimo_cambio_costo.strftime("%d/%m/%y")
                if product.np_ultimo_cambio_costo
                else "",  # 22 ultimo cambio costo (formato dd/mm/yy)
                product.np_observaciones or "",  # 23 observaciones
            ]
            writer.writerow(row)

        csv_content = output.getvalue().encode("utf-8")
        output.close()

        # Crear attachment para descarga
        attachment = self.env["ir.attachment"].create(
            {
                "name": "productos_nota_pedido.csv",
                "type": "binary",
                "datas": base64.b64encode(csv_content),
                "res_model": "product.template",
                "res_id": 0,
                "mimetype": "text/csv",
            }
        )

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/?model=ir.attachment&id={attachment.id}&field=datas&filename_field=name&download=true",
            "target": "self",
        }
