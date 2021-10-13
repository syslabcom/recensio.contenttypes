jQuery(function ($) {
    $(document).on('click', '[id^=atrb_] form#create input[name=submit]', function (event) {
    event.preventDefault();
    var target = $(event.target);
    var src = target.parents('form').attr('action');
    var wrap = target.parents('.overlaycontent');
    var firstname = wrap.find('input[name=firstname]').attr('value');
    var lastname = wrap.find('input[name=lastname]').attr('value');
    $.post(src, {firstname: firstname, lastname: lastname}, function (data) {
        /* Solr needs some time to commit */
        setTimeout(function () {
            wrap.find('form#search input#searchGadget').attr('value', [lastname, firstname].filter(Boolean).join(' '));
            wrap.find('form#search input.searchButton').click();
        }, 1500);
    });
    });
});

