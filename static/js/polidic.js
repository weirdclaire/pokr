(function () {

// event triggers
if (!isMobile) {
    $('a.person-link').live('click.linkPerson', function (e) {
        var $this = $(this);

        // Preserve hashtag if the current page is of a person
        if (window.currentPage == 'person' && location.hash) {
            location.href = $this.attr('href') + location.hash;
            return false;
        }
    });
}

/* Warm-up scripts */
$(window).load(onLoad);

function onLoad() {
    $('.person-img').clipImage();
    if (!isMobile) {
        $('.tooltipped:not(.tooltipped-delay)').tooltip();
        $('.tooltipped-delay').tooltip({
            delay: {
                show: 3000,
                hide: 0
            }
        });
    }

    $('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id], .anchor').each(function () {
        var $this = $(this),
            target = $this.data('target-id') || $this.attr('id');
        $('<a class="permalink" href="#'+target+'"><i class="icon-link"></i></a>').appendTo($this);
    });
};

}());
