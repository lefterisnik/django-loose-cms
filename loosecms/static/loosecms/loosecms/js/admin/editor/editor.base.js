(function($) {
    'use strict';

    $(document).ready(function() {
        $('body').prepend('<span class="glyphicon glyphicon-menu-right sb-toggle-left" aria-hidden="true"></span>');

        // using jQuery
        var slidebar = new $.slidebars();
        $("#menu").metisMenu();

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = $.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        function caclulate_height(iframe){
            if (iframe.contentWindow.document.body.offsetHeight > $(window).height() - 50){
                return $(window).height()*2/3;
            }
            else{
                return iframe.contentWindow.document.body.offsetHeight + 50 + 'px';
            }
        }

        function make_jspanel(url) {

            var panel = $.jsPanel({
                show: "fadeOut",
                size: {
                    width: function(){ return $(window).width()*(2/3) },
                    height: 'auto',
                },
                controls: { minimize: 'disable', iconfont: "bootstrap" },
                position: "top center",
                bootstrap: 'primary',
                addClass:{
                    content: "custom-content",
                },
                iframe: {
                    src:    url,
                    style:  {"border": "solid transparent"},
                    width:  '100%',
                    height: '100%',
                },
                callback: function (panel) {
                    $("iframe", panel).load(function (e) {
                        $(e.target).fadeIn(2000);
                        panel.content.css({"width": "auto", "height": "auto"});
                        panel.fadeIn();
                        panel.resize(null, caclulate_height(this));
                        panel.reposition("top center");
                        panel.title(this.contentWindow.document.title);
                    });
                }
            });
        }

        /**************************************Edit style**********************************************/

        $('body').on('click', '.loosecms-plugin', function( e ) {
            e.preventDefault();

            if (slidebar.slidebars.active('left')){
                slidebar.slidebars.toggle('left');
            }

            var url = $(this).attr('href');

            make_jspanel(url);
        });

        /**************************************Add page***********************************************/

        $('body').on('click', '.add-page', function( e ) {
            e.preventDefault();

            if (slidebar.slidebars.active('left')){
                slidebar.slidebars.toggle('left');
            }

            var url = $(this).attr('href');
            var type = $(this).data('type');
            var template = $(this).data('template');
            var slug = $(this).data('slug');

            if (slug === undefined){
                slug = '';
            }


            if (template === undefined){
                url = url + '?type=' + type + '&slug=' + slug;
            }
            else{
                url = url + '?type=' + type + '&slug=' + slug + '&is_template=' + template;
            }

            make_jspanel(url);
        });

        /**************************************Edit page***********************************************/

        $('body').on('click', '.edit-page', function(e){
            e.preventDefault();

            if (slidebar.slidebars.active('left')){
                slidebar.slidebars.toggle('left');
            }

            var url = $(this).attr('href');

            make_jspanel(url);

        });

        /**************************************Add plugin***********************************************/

        $('body').on('click', '.add-plugin', function( e ) {
            e.preventDefault();

            if (slidebar.slidebars.active('left')){
                slidebar.slidebars.toggle('left');
            }

            var url = $(this).attr('href');
            var type = $(this).data('type');
            var placeholder = $(this).data('placeholder');

            if (placeholder === undefined) {
                url = url + '?type=' + type;
            }
            else {
                url = url + '?type=' + type + '&placeholder=' + placeholder;
            }

            make_jspanel(url);

        });

        /**************************************Edit plugin***********************************************/

        $('body').on('click', '.edit-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            make_jspanel(url);
        });

        /**************************************Delete plugin***********************************************/

        $('body').on('click', '.delete-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            make_jspanel(url);
        });

        /**************************************Move plugin***********************************************/

        $('body').on('click', '.move-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            make_jspanel(url);
        });

        /**************************************Select plugin*********************************************/

        $('body').on('click', '.select-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            make_jspanel(url);
        });

        /**************************************Remove plugin*********************************************/

        $('body').on('click', '.remove-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            $.ajax({
                method: "DELETE",
                url: url,
                success: function( data, textStatus, jqXHR) {
                    location.reload();
                },
                error: function( jqXHR, textStatus, errorThrown) {
                    alert(errorThrown + jqXHR.responseText);
                },
            });
        });

        /***********************************Change dropdown to dropup************************************/

        var dropup = function()  {
            $(".dropdown-toggle").each(function(){
                var par=$(this).parents('.btn-group');
                var dropl=par.find('ul');
                var otop=$(this).offset().top+$(this).height()-$(window).scrollTop();
                var ulh=dropl.height();
                var obot=$(window).height()-$(this).height()-$(this).offset().top+$(window).scrollTop();

                if ((obot < ulh) && (otop > ulh)) {
                    par.addClass('dropup');
                } else {
                    par.removeClass('dropup');
                }

            });
        }

        $(window).load(dropup);
        $(window).bind('resize', dropup);
        /*$(window).bind('resize scroll touchstart touchmove mousewheel', dropup);*/

    });

}) (jQuery);
