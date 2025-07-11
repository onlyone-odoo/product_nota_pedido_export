===========
Product Nota de Pedido Export
===========

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3


|badge1| |badge2| |badge3| 

This module extends the functionality of product management to support custom fields from the Nota de Pedido system and to allow you to export products to a CSV file in a specific format with '|' separator.

**Table of contents**

.. contents::
   :local:

Configure
=========

To configure this module, you need to:

Go to Inventory > Configuration > Products and fill in the custom fields in the "DATOS NOTA DE PEDIDO" tab for each product template.

Usage
=====

1. Go to a product template form view.
2. Navigate to the "DATOS NOTA DE PEDIDO" tab and enter the required custom data (e.g., rubro, familia, precios, etc.).
3. To export, add a button to the view calling the method 'export_products_to_csv' or run it via a server action.

Known issues / Roadmap
======================

* No known issues at this time.
* Roadmap: Integrate dynamic currency rates from res.currency for better cotización handling.

Bug Tracker
===========

* Help Contact: support@onlyone.odoo.com

Credits
=======

Authors
~~~~~~~

* Be OnlyOne

Contributors
~~~~~~~~~~~~

* `Be OnlyOne. <https://onlyone.odoo.com/>`_
  
  * Matías Bressanello

Maintainers
~~~~~~~~~~~

This module is maintained by Be OnlyOne 