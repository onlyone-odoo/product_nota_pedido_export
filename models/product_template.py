# models/product_template.py
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Campos NDP (prefijo ndp_ para evitar conflictos)
    ndp_rubro = fields.Char(string="Rubro")
    ndp_nombre_rubro = fields.Char(string="Nombre del Rubro")
    ndp_sku = fields.Char(string="SKU (Código SIEL)")  # Clave para match
    ndp_nombre_producto = fields.Char(
        string="Nombre Producto", compute="_compute_nombre_producto", store=True
    )
    ndp_familia = fields.Char(string="Familia")
    ndp_codigo_area = fields.Char(string="Código de Área")
    ndp_nombre_area = fields.Char(string="Nombre del Área")
    ndp_precio_publico_moneda = fields.Float(
        string="Precio Público (Moneda)", compute="_compute_precios"
    )
    ndp_precio_mayorista_moneda = fields.Float(
        string="Precio Mayorista (Moneda)", compute="_compute_precios"
    )
    ndp_iva_porcentaje = fields.Float(
        string="% IVA", related="taxes_id.amount", store=True
    )  # De taxes
    ndp_unidad_medida = fields.Char(string="Unidad de Medida", related="uom_id.name")
    ndp_nombre_foto = fields.Char(string="Nombre Archivo Foto")
    ndp_codigo_barra = fields.Char(string="Código Barra", related="barcode")
    ndp_moneda = fields.Selection(
        [("DO", "Dólar"), ("PE", "Pesos")], string="Moneda", default="PE"
    )
    ndp_precio_publico_pesos = fields.Float(
        string="Precio Público $", compute="_compute_precios_pesos"
    )
    ndp_precio_mayorista_pesos = fields.Float(
        string="Precio Mayorista $", compute="_compute_precios_pesos"
    )
    ndp_cotizacion_dolar = fields.Float(
        string="Cotización Dólar", compute="_compute_cotizacion_dolar"
    )
    ndp_stock = fields.Float(string="Stock", compute="_compute_stock")
    ndp_costo = fields.Float(string="Costo", related="standard_price")
    ndp_pto_pedido = fields.Float(string="Pto Pedido", related="reordering_min_qty")
    ndp_url_web = fields.Char(string="URL Web")
    ndp_ultimo_cambio_costo = fields.Date(string="Último Cambio Costo")
    ndp_observaciones = fields.Text(string="Observaciones")

    @api.depends("name")
    def _compute_nombre_producto(self):
        for rec in self:
            rec.ndp_nombre_producto = rec.name

    @api.depends(
        "list_price",
    )
    @api.depends("list_price")
    def _compute_precios(self):
        publico_pricelist_usd = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Minorista USD"),
                ("company_id", "=", self.env.company.id),
            ]
        )
        mayorista_pricelist_usd = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Mayorista USD"),
                ("company_id", "=", self.env.company.id),
            ]
        )
        publico_pricelist = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Minorista ARS"),
                ("company_id", "=", self.env.company.id),
            ]
        )
        mayorista_pricelist = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Mayorista ARS"),
                ("company_id", "=", self.env.company.id),
            ]
        )

        for rec in self:
            if rec.ndp_moneda == "DO":
                rec.ndp_precio_publico_moneda = (
                    publico_pricelist_usd._get_product_price(rec, 1.0)
                )
                rec.ndp_precio_mayorista_moneda = (
                    mayorista_pricelist_usd._get_product_price(rec, 1.0)
                )
            else:
                rec.ndp_precio_publico_moneda = publico_pricelist._get_product_price(
                    rec, 1.0
                )
                rec.ndp_precio_mayorista_moneda = (
                    mayorista_pricelist._get_product_price(rec, 1.0)
                )

    @api.depends(
        "ndp_precio_publico_moneda",
        "ndp_precio_mayorista_moneda",
        "ndp_moneda",
        "ndp_cotizacion_dolar",
    )
    def _compute_precios_pesos(self):
        publico_pricelist_usd = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Minorista USD"),
                ("company_id", "=", self.env.company.id),
            ]
        )
        mayorista_pricelist_usd = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Mayorista USD"),
                ("company_id", "=", self.env.company.id),
            ]
        )
        publico_pricelist = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Minorista ARS"),
                ("company_id", "=", self.env.company.id),
            ]
        )
        mayorista_pricelist = self.env["product.pricelist"].search(
            [
                ("name", "=", "Precio Mayorista ARS"),
                ("company_id", "=", self.env.company.id),
            ]
        )

        for rec in self:
            if rec.ndp_moneda == "DO":
                rec.ndp_precio_publico_pesos = publico_pricelist._get_product_price(
                    rec, 1.0
                )
                rec.ndp_precio_mayorista_pesos = mayorista_pricelist._get_product_price(
                    rec, 1.0
                )
            else:
                rec.ndp_precio_publico_pesos = rec.ndp_precio_publico_moneda
                rec.ndp_precio_mayorista_pesos = rec.ndp_precio_mayorista_moneda

    @api.depends("company_id")
    def _compute_cotizacion_dolar(self):
        _logger.info(
            f"Se esta ejecutando _compute_cotizacion_dolar esto es self: {self}. "
        )
        usd = self.env.ref("base.USD")
        _logger.info(
            f"Se esta ejecutando _compute_cotizacion_dolar esto es usd: {usd}. "
        )
        ars = self.env.ref("base.ARS")
        _logger.info(
            f"Se esta ejecutando _compute_cotizacion_dolar esto es ars: {ars}. "
        )
        for rec in self:
            # Buscar la tasa para la compañía del registro
            rate = self.env["res.currency.rate"].search(
                [("currency_id", "=", usd.id), ("company_id", "=", rec.company_id.id)],
                limit=1,
                order="name desc",
            )
            _logger.info(
                f"Se esta ejecutando _compute_cotizacion_dolar esto es rate: {rate}. "
            )
            if not rate or not rate.rate or rate.rate <= 0:
                # Fallback: buscar tasa sin restringir por compañía
                rate = self.env["res.currency.rate"].search(
                    [("currency_id", "=", usd.id)],
                    limit=1,
                    order="name desc",
                )
            # Asignar el valor: tasa válida, o 1.0 como fallback
            rec.ndp_cotizacion_dolar = rate.rate if rate and rate.rate > 0 else 1.0
            # Log para depuración
            if not rate or not rate.rate or rate.rate <= 0:
                _logger.info(
                    f"No se encontró una tasa válida para USD en la compañía {rec.company_id.name}. "
                    f"Usando valor por defecto: 1.0"
                )

    @api.depends("qty_available")
    def _compute_stock(self):
        for rec in self:
            rec.ndp_stock = (
                rec.qty_available
            )  # O usa stock.quant para warehouse específico
