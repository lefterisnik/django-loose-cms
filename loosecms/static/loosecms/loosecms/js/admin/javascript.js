(function($) {
    $(document).ready(function() {
        // using jQuery
        var slidebar = new $.slidebars();
        $("#menu").metisMenu();

        var add_page;
        var edit_page;
        var add_panel;
        var edit_panel;
        var delete_panel;
        var edit_style;

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = $.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
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
                return iframe.contentWindow.document.body.offsetHeight + 35 + 'px';
            }
        }

        /**************************************Edit style**********************************************/

        $('body').on('click', '.edit-style', function( e ) {
            e.preventDefault();

            if (slidebar.slidebars.active('left')){
                slidebar.slidebars.toggle('left');
            }

            var url = $(this).attr('href');

            edit_style = $.jsPanel({
                position: "top center",
                bootstrap: 'primary',
                addClass:{
                    content: "custom-content edit-style-form",
                },
                ajax: {
                    url: url,
                    done: function ( data, textStatus, jqXHR, jsPanel ){
                        jsPanel.content.css({"width": "auto",
                                            "min-height": "500px",
                                            "padding": "10px 15px"});
                        jsPanel.resize("auto", "auto");
                        jsPanel.reposition("top center");
                        jsPanel.title($(data).find('span.navbar-brand').html());
                    },
                    fail:   function( jqXHR, textStatus, errorThrown, jsPanel ){
                        jsPanel.content.append(jqXHR.responseText);
                    },
                },
            });
        });

        $('body').on('submit', '.edit-style-form form', function(e){
            e.preventDefault();

            var formData = new FormData($(this)[0]);

            $.ajax({
                method: "POST",
                url: $(this).attr('action'),
                data: formData,
                processData: false, // Don't process the files
                contentType: false, // Set content type to false as jQuery will tell the server its a query string request
                success: function( data, textStatus, jqXHR) {
                    if(data && typeof data.redirect_url != 'undefined'){
                        location.reload();
                    } else {
                        edit_style.content.html(data);
                    }
                },
                error: function( jqXHR, textStatus, errorThrown) {
                    alert(errorThrown + jqXHR.responseText);
                },
            });

        });

        $('body').on('click', '.closeTab', function(e){
            //there are multiple elements which has .closeTab icon so close the tab whose close icon is clicked
            var tabContentId = $(this).parent().attr("href");
            $(this).parent().parent().remove(); //remove li of tab
            $('#myTab a:last').tab('show'); // Select first tab
            $(tabContentId).remove(); //remove respective tab content
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
            var slug = $(this).data('slug')

            if (slug === undefined){
                slug = '';
            }


            if (template === undefined){
                url = url + '?type=' + type + '&slug=' + slug;
            }
            else{
                url = url + '?type=' + type + '&slug=' + slug + '&is_template=' + template;
            }

            $.jsPanel({
                size: {
                    width: function(){ return $(window).width()*(2/3) },
                    height: 'auto'
                },
                controls: { iconfont: "bootstrap" },
                position: "top center",
                bootstrap: 'primary',
                addClass:{
                    content: "custom-content",
                },
                iframe: {
                    src:    url,
                    style:  {"border": "solid transparent"},
                    width:  '100%',
                    height: '100%'
                },
                callback: function (panel) {
                    $("iframe", panel).load(function (e) {
                        $(e.target).fadeIn(2000);
                        this.style.height = this.contentWindow.document.body.offsetHeight + 35 + 'px';
                        panel.resize(null, caclulate_height(this));
                        panel.reposition("top center");
                        panel.title(this.contentWindow.document.title);
                    });
                }
            });
        });

        /**************************************Edit page***********************************************/

        $('body').on('click', '.edit-page', function(e){
            e.preventDefault();

            if (slidebar.slidebars.active('left')){
                slidebar.slidebars.toggle('left');
            }

            var url = $(this).attr('href');

            $.jsPanel({
                size: {
                    width: function(){ return $(window).width()*(2/3) },
                    height: 'auto'
                },
                controls: { iconfont: "bootstrap" },
                position: "top center",
                bootstrap: 'primary',
                addClass:{
                    content: "custom-content",
                },
                iframe: {
                    src:    url,
                    style:  {"border": "solid transparent"},
                    width:  '100%',
                    height: '100%'
                },
                callback: function (panel) {
                    $("iframe", panel).load(function (e) {
                        $(e.target).fadeIn(2000);
                        this.style.height = this.contentWindow.document.body.offsetHeight + 35 + 'px';
                        panel.resize(null, caclulate_height(this));
                        panel.reposition("top center");
                        panel.title(this.contentWindow.document.title);
                    });
                }
            });

        });

        /**************************************Add plugin***********************************************/

        $('body').on('click', '.add-plugin', function( e ) {
            e.preventDefault();

            if (slidebar.slidebars.active('left')){
                slidebar.slidebars.toggle('left');
            }

            var url = $(this).attr('href');
            var current_url = $(location).attr('href');
            var type = $(this).data('type');
            var placeholder = $(this).data('placeholder');

            if (placeholder === undefined) {
                url = url + '?type=' + type;
            }
            else {
                url = url + '?type=' + type + '&placeholder=' + placeholder;
            }

            $.jsPanel({
                size: {
                    width: function(){ return $(window).width()*(2/3) },
                    height: 'auto'
                },
                controls: { iconfont: "bootstrap" },
                position: "top center",
                bootstrap: 'primary',
                addClass:{
                    content: "custom-content",
                },
                iframe: {
                    src:    url,
                    style:  {"border": "solid transparent"},
                    width:  '100%',
                    height: '100%'
                },
                callback: function (panel) {
                    $("iframe", panel).load(function (e) {
                        $(e.target).fadeIn(2000);
                        this.style.height = this.contentWindow.document.body.offsetHeight + 35 + 'px';
                        panel.resize(null, caclulate_height(this));
                        panel.reposition("top center");
                        panel.title(this.contentWindow.document.title);
                    });
                }
            });
        });

        /**************************************Edit plugin***********************************************/

        $('body').on('click', '.edit-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            $.jsPanel({
                size: {
                    width: function(){ return $(window).width()*(2/3) },
                    height: 'auto'
                },
                controls: { iconfont: "bootstrap" },
                position: "top center",
                bootstrap: 'primary',
                iframe: {
                    src:    url,
                    style:  {"border": "solid transparent"},
                    width:  '100%',
                    height: '100%'
                },
                callback: function (panel) {
                    $("iframe", panel).load(function (e) {
                        $(e.target).fadeIn(2000);
                        this.style.height = this.contentWindow.document.body.offsetHeight + 35 + 'px';
                        panel.resize(null, caclulate_height(this));
                        panel.reposition("top center");
                        panel.title(this.contentWindow.document.title);
                    });
                }
            });
        });

        /**************************************Delete plugin***********************************************/

        $('body').on('click', '.delete-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            $.jsPanel({
                size: {
                    width: function(){ return $(window).width()*(2/3) },
                    height: 'auto'
                },
                controls: { iconfont: "bootstrap" },
                position: "top center",
                bootstrap: 'primary',
                iframe: {
                    src:    url,
                    style:  {"border": "solid transparent"},
                    width:  '100%',
                    height: '100%'
                },
                callback: function (panel) {
                    $("iframe", panel).load(function (e) {
                        $(e.target).fadeIn(2000);
                        this.style.height = this.contentWindow.document.body.offsetHeight + 35 + 'px';
                        panel.resize(null, caclulate_height(this));
                        panel.reposition("top center");
                        panel.title(this.contentWindow.document.title);
                    });
                }
            });
        });


        /**************************************Move plugin***********************************************/

        $('body').on('click', '.move-plugin', function(e){
            e.preventDefault();

            var url = $(this).attr('href');

            $.jsPanel({
                size: {
                    width: function(){ return $(window).width()*(2/3) },
                    height: 'auto'
                },
                controls: { iconfont: "bootstrap" },
                position: "top center",
                bootstrap: 'primary',
                iframe: {
                    src:    url,
                    style:  {"border": "solid transparent"},
                    width:  '100%',
                    height: '100%'
                },
                callback: function (panel) {
                    $("iframe", panel).load(function (e) {
                        $(e.target).fadeIn(2000);
                        this.style.height = this.contentWindow.document.body.offsetHeight + 35 + 'px';
                        panel.resize(null, caclulate_height(this));
                        panel.reposition("top center");
                        panel.title(this.contentWindow.document.title);
                    });
                }
            });
        });
    });

}) (django.jQuery);
