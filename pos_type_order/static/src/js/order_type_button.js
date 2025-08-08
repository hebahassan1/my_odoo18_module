console.log('loadddddddddddddddddddddd');
import { Component, useState, xml } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { rpc } from "@web/core/network/rpc";

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";


patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        self = this;
        this.ui = useState(useService("ui"));
        self.currentOrder.update({ pos_type_order_id: {'id':1,'name':'Normal'} });
       
        
    },
    
     get currentOrder() {
        return this.pos.get_order();
    },

    async onClickSelectOrderType() {
          
        const order_types = this.env
        const resIds= await this.env.services.orm.search("pos.type.order", [["active", "=", true]]);
        console.log(resIds);
        console.log('//////////');
        if (resIds.length > 0) {
            const fields = ['id','name'];  // specify the fields you want to fetch
            const availtype = await this.env.services.orm.read("pos.type.order", resIds, fields);
            console.log(availtype);
            const availableType = availtype.filter(posordertype => posordertype.name !== 'Normal').map(posordertype => ({
                id: posordertype.id,
                label: posordertype.name,
                item: posordertype,
            }));
            const payload = await makeAwaitable(this.dialog, SelectionPopup, {
                title: " Available Order Types",
                list: availableType,
            });
            if (payload) {
            
              self.currentOrder.update({ pos_type_order_id: payload });
              document.querySelector('#ordertype_id').textContent= "  " + payload['name'];
              document.querySelector('#posordertypebtn').style.backgroundColor = 'green';
              document.querySelector('#posordertypebtn').style.color = 'white';

            }
        }
      
    }
   
});
