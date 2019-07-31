/******************************************************************************
    Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
    @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 *****************************************************************************/
'use strict';

openerp.pos_environment = function(instance, local) {

    var module = instance.point_of_sale;

    /*************************************************************************
        Extend module.Order:
            add environment header and footer in export_for_printing
            to make print via proxy working
    */
    var moduleOrderParent = module.Order;
    module.Order = module.Order.extend({

        export_for_printing: function(attributes){
            var order = moduleOrderParent.prototype.export_for_printing.apply(this, arguments);
            order.receipt_environment_header = this.pos.config.receipt_environment_header;
            order.receipt_environment_footer = this.pos.config.receipt_environment_footer;
            return order;
        },

    });

};
