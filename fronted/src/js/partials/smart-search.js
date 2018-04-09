$(document).ready( function() {
    //ПОИСК
    var timeout;
    var printing = 0;

    $("[data-search-input]").on('keyup',function(e){
        var $this = $(this);

        if (!(e.ctrlKey && e.keyCode == 13) && !(!e.ctrlKey && e.keyCode == 17)) {

            printing = printing + 1;

            // Вызываем, только если изменилось значение
            if (printing == 1) {
                setTimeout(function() {
                    console.log("Начал ввод...")
                },100);
            }

            if (printing != 0) {
                // Делаем задержку и обнуляем предыдущую
                if(timeout) { clearTimeout(timeout); }
                // Новый таймаут
                timeout = setTimeout(function() {
                    // Выполняем поиск
                    console.log("Закончил ввод...");
                    load_results($this.data('ajax-url'), $this.val().toLowerCase());
                    printing = 0;
                },500);
            }
        }
    });

    function load_results(ajax_url, search_val) {
        var result_el = $('.smart-search__search-result');
        // Ищем
        $.get(ajax_url, { startswith: search_val }, function (data) {
            if(data.items) {
                data.items.forEach(function (item, i, arr) {
                    var date = moment(item['date']);
                    // Подменяем исходную дату, форматированной и лоализованной, согласен не очень красиво, но увы, мусташ не совершенен
                    item['date'] = date.locale('ru').format('Do MMMM YYYY, H:mm:ss')
                })
            }
            var template = $('.mustache-search-results').html();
            var rendered = Mustache.render(template, data); // Рендерим темплейт через мусташ
            result_el.html(rendered);
        });
    }
});