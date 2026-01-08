odoo.define('odoo_saas_kit_trial.saas_trial_contract_portal', function(require){
    "user strict";
    var ajax = require('web.ajax');

    $(document).ready(function() {
        $('.o_portal_wrap').each(function() {
            $('#button_submit').click(function(){
                var contract_id = $('#pay_for_trial').attr('value');
                var radio_1 = $('#radio_1').is(':checked');
                var radio_2 = $('#radio_2').is(':checked');
                if (radio_1){
                    var new_contract = false;
                    ajax.jsonRpc('/saa/trial/pay_now', 'call', {
                        contract_id: parseInt(contract_id),
                        from_trial: true,
                        new_contract: new_contract,
                    }).then(function(){
                        location.href="/shop/cart";
                    });
                }
                else if(radio_2){
                    var new_contract = true;
                    ajax.jsonRpc('/saa/trial/pay_now', 'call', {
                        contract_id: parseInt(contract_id),
                        from_trial: true,
                        new_contract: new_contract,
                    }).then(function(){
                        location.href="/shop/cart";
                    });
                }
            }); 
            
        });
    });



});