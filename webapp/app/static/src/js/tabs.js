$(document).ready(function(){
    var hash = window.location.hash;
    if(hash){
        $('.nav-item a.nav-link[role="tab"][href="' + hash + '"]').tab('show');
    }

    $('.nav-item a.nav-link[role="tab"]').on('shown.bs.tab', function(event){
        window.location.hash = $(this).attr('href');
    });

    $(window).on('popstate', function() {
        var hash = window.location.hash;
        if(hash){
            $('.nav-item a.nav-link[role="tab"][href="' + hash + '"]').tab('show');
        } else {
            $('.nav-item a.nav-link[role="tab"][href="#home"]').tab('show');
        }
    });
});