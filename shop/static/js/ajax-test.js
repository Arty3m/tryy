$(document).ready(function () {
    $('#sort').on('change', function () {
        var sortBy = $(this).val();
        var brandFilter = $('#brand-filter').val();
        var priceFilter = $('#price-filter').val();
        var url = '/a2?sort=' + sortBy + '&brand=' + brandFilter + '&price=' + priceFilter;
        console.log(sortBy);
        $.ajax({
            url: url,
            type: 'GET',
            success: function (response) {
                // Обновление списка продуктов на странице
                $('#product-list').html(response);
            }
        });
    });

    $('#brand-filter').on('change', function () {
        // Аналогично для изменения фильтра по бренду
    });

    $('#price-filter').on('change', function () {
        // Аналогично для изменения фильтра по цене
    });
});
