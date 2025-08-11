import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { OrderTabs } from "@point_of_sale/app/components/order_tabs/order_tabs";

// Patch Order to have its own reactive selectedOrderType
const superSelectFloatingOrder = OrderTabs.prototype.selectFloatingOrder;

patch(PosStore.prototype, {
  createNewOrder() {
        const order = super.createNewOrder(...arguments);
        
        if(order.pos_type_order_id==undefined)
         {
             order.selectedOrderType = { id: 1, name: 'Normal' }; 
             order.pos_type_order_id= { id: 1, name: 'Normal' } ;
            // order.update({ pos_type_order_id: {id:order.selectedOrderType.id,name:order.selectedOrderType.name} });
         }


        return order;
    },
});

patch(OrderTabs.prototype ,{

    async selectFloatingOrder(order) {
        await superSelectFloatingOrder.call(this, order);
        if(order.pos_type_order_id==undefined && order.selectedOrderType ==undefined)
          {
              order.pos_type_order_id= { id: 1, name: 'Normal' };
              order.selectedOrderType = { id: 1, name: 'Normal' };
          }
        else if(order.pos_type_order_id && order.selectedOrderType ==undefined)
          {
              order.selectedOrderType = {id:order.pos_type_order_id.id,name:order.pos_type_order_id.name}; 
          }
          else if(order.pos_type_order_id == undefined && order.selectedOrderType)
          {
             order.pos_type_order_id = {id:order.selectedOrderType.id,name:order.selectedOrderType.name}; 
             //order.update({ pos_type_order_id:  {id:order.selectedOrderType.id,name:order.selectedOrderType.name}});
          }
    }

});
function setupSharedState(self) {
    self.pos = usePos();
    self.ui = useState(useService("ui"));
    self.is_ot_in_product = self.pos.config.is_ot_in_product;
    self.is_ot_in_payment = self.pos.config.is_ot_in_payment;
}

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        setupSharedState(this);
    },
    get currentOrder() {
        return this.pos.get_order();
    },
    onClickSelectOrderType,
});

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        setupSharedState(this);
    },
    get currentOrder() {
        return this.pos.get_order();
    },
    onClickSelectOrderType,
});

async function onClickSelectOrderType() {
    const resIds = await this.env.services.orm.search("pos.type.order", [["active", "=", true]]);
    if (resIds.length > 0) {
        const availtype = await this.env.services.orm.read("pos.type.order", resIds, ["id", "name"]);
        const availableType = availtype
            .filter(type => type.name !== "Normal")
            .map(type => ({
                id: type.id,
                label: type.name,
                item: type,
            }));
        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: "Available Order Types",
            list: availableType,
        });
        if (payload) {
            this.currentOrder.selectedOrderType ={id:payload.id,name:payload.name};
            this.currentOrder.pos_type_order_id ={id:payload.id,name:payload.name};

            //this.currentOrder.update({ pos_type_order_id: payload });
        }
    }
}

