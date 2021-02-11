/** ****************************************************************************
    Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
    @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 *****************************************************************************/

odoo.define('pos_environment.models', function (require) {
    'use strict';

    var models = require('point_of_sale.models');

    var order_super = models.Order.prototype;

    models.Order = models.Order.extend({
        export_for_printing: function () {
            var res = order_super.export_for_printing.apply(this, arguments);
            res.receipt_environment_header =
                this.pos.config.receipt_environment_header;
            res.receipt_environment_footer =
                this.pos.config.receipt_environment_footer;
            return res;
        },
    });
});
