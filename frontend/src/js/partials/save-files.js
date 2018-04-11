$(document).ready( function() {

    // Парсим результаты поиска и сохраняем в zip архив
    $(document).on('click', '[data-save-zip]', function(e) {
        var zip = new JSZip();
        var results = $('.results-list .result:visible');

        var csvContent = "date;from;subject;msg\r\n";
        results.each(function (i, item, arr) {
            var row = [];
            $(item).find('div').each(function (i, item, arr) {
                row.push($(item).html())
            });

            csvContent += row.join(';') + "\r\n";
        });

        zip.file('email.csv', csvContent);

        zip.generateAsync({type:"blob"})
            .then(function(content) {
                saveAs(content, "emails.zip");
            });

    });
});