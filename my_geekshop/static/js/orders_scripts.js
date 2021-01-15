$(document).ready(function () {
    // When document ready
    var $order_total_quantity = $(".order_total_quantity");
    var $order_total_cost = $(".order_total_cost");
    // Current state structure
    var $currentState = $(".formset_row").clone();

    function renewSummary() {
        if ($(".formset_row").length) {
            var quantitySummary = 0;
            var costSummary = 0;
            $(".formset_row").each(function () {
                if ($(this).css("display") != "none" ){
                    var quantity = parseInt($(this).find("input[type='number']").val());
                    if (quantity) {
                        quantitySummary += quantity;
                        costSummary += parseFloat(
                            Number(
                                parseFloat(
                                    $(this).find("[class^=orderitems]").text()
                                ) * quantity
                            ).toFixed(2)
                        );
                    };
                };
            });
            $order_total_quantity.text(quantitySummary);
            $order_total_cost.text(Number(costSummary).toFixed(2));
        };
    };

    $("input[type='number']").change(function () {
        var $price_object = $(this).parent().parent().find("[class^=orderitems]");
        if (!$price_object.length) {
            var item_price = 0;
        } else {
            var item_price = parseFloat($price_object.text());
        };
        var quantity_delta = $(this).val() - $currentState.find("[name=" + $(this).attr("name") + "]").val();
        $order_total_quantity.text(parseInt($order_total_quantity.text()) + quantity_delta);
        $order_total_cost.text(Number(parseFloat($order_total_cost.text()) + quantity_delta * item_price).toFixed(2));
        // Renew current state structure
        $currentState = $(".formset_row").clone();
    });

    $("select[name^=orderitems]").change(function () {
        var $currenElement = $(this);
        $.ajax({
            url: "/order/product/" + $currenElement.val() + "/price/",
            success: function (data) {
                var $formParent = $currenElement.parent().parent().find(".td3");
                var priceSpan = document.createElement("span");
                priceSpan.classList.add("orderitems");
                priceSpan.innerText = data.price
                $formParent.html("");
                $formParent.append(priceSpan).append(" руб");
                $currenElement.parent().parent().find("input[type='number']").prop('disabled', false);
                renewSummary();
                // Renew current state structure
                $currentState = $(".formset_row").clone();
            },
        });

    });

    function setDefaultValue() {
        // Set default value for new forms
        $("input[type='number']").each(function () {
            if (!$(this).val()) {
                $(this).val(0).prop('disabled', true);
                $(this).parent().parent().find(".td3").html("");
                $(this).parent().parent().find("select").find("option:first").prop("selected", true);
            };
        });
        // Renew current state structure
        $currentState = $(".formset_row").clone();
    };

    function itemDelete(row) {
        var quantity_delta = parseInt($(row).find("[type='number']").val());
        $order_total_quantity.text(parseInt($order_total_quantity.text()) - quantity_delta);
        var $price_object = $(row).find("[class^=orderitems]");
        if (!$price_object.length) {
            var item_price = 0;
        } else {
            var item_price = parseFloat($price_object.text());
        };
        $order_total_cost.text(Number(parseFloat($order_total_cost.text()) - quantity_delta * item_price).toFixed(2));
        if ($(".formset_row").length) {
            $currentState = $(".formset_row").clone();
        } else {
            $order_total_quantity.text(0);
            $order_total_cost.text(0);
        };
    };

    $('.formset_row').formset({
        addText: 'Добавить продукт',
        addCssClass: 'btn btn-default btn-block',
        deleteText: 'Удалить',
        deleteCssClass: 'btn btn-warning',
        prefix: 'orderitems',
        added: setDefaultValue,
        removed: itemDelete,
        hideLastAddForm: true
    });

    // Fix formsets display --->
    $(".formset_row").each(function () {
        if ($(this).find("span[class*='price']").text()) {
            $(this).css("display", "");
        };
    });
    // <--- Fix formsets display

    renewSummary();
});
