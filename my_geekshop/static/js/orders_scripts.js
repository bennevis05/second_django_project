$(document).ready(function(){
    // When document ready
    var $order_total_quantity = $(".order_total_quantity");
    var $order_total_cost = $(".order_total_cost");
    // Current state structure
    var $currentState = $(".formset_row").clone();

    $("input[type='number']").change(function(){
        var $price_object = $(this).parent().parent().find("[class^=orderitems]");
        if (!$price_object.length) {
            var item_price = 0;
        } else {
            var item_price = parseFloat($price_object.text());
        };
        var quantity_delta = $(this).val() - $currentState.find("[name=" + $(this).attr("name") + "]").val();
        $order_total_quantity.text( parseInt($order_total_quantity.text()) + quantity_delta);
        $order_total_cost.text( Number(parseFloat($order_total_cost.text()) + quantity_delta * item_price).toFixed(2) );
        // Renew current state structure
        $currentState = $(".formset_row").clone();
    });

    function setDefaultValue() {
        // Set default value for new forms
        $("input[type='number']").each(function(){
            if (!$(this).val()){
                $(this).val(0);
            };
        });
        // Renew current state structure
        $currentState = $(".formset_row").clone();
    };

    function itemDelete( row ) {
        var quantity_delta = parseInt($(row).find("[type='number']").val());
        $order_total_quantity.text( parseInt($order_total_quantity.text()) - quantity_delta);
        var $price_object = $(row).find("[class^=orderitems]");
        if (!$price_object.length) {
            var item_price = 0;
        } else {
            var item_price = parseFloat($price_object.text());
        };
        $order_total_cost.text( Number(parseFloat($order_total_cost.text()) - quantity_delta * item_price).toFixed(2) );
        $currentState = $(".formset_row").clone();
    };

    $('.formset_row').formset({
        addText: 'Добавить продукт',
        addCssClass: 'btn btn-default btn-block',
        deleteText: 'Удалить',
        deleteCssClass: 'btn btn-warning',
        prefix: 'orderitems',
        added: setDefaultValue,
        removed: itemDelete,
    });
});
