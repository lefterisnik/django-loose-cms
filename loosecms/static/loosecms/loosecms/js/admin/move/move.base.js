(function($) {
    $(document).ready(function() {

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


        /******************************Filter move dialog***********************************/

        $('body').on('change', '#id_new_page', function(e){
            e.preventDefault();

            var new_placeholder = $('#id_new_placeholder')

            var attrs = window.location.href.split('/');
            var api_url = filter_move_choices + attrs[attrs.length-2] + '/';
            api_url = api_url + '?selected_page=' + this.value;


            $.ajax({
                url: api_url,
                dataType: 'json',
            })

            .success(function(data){
                new_placeholder.empty();
                var option = new Option('---------', '');
                new_placeholder.append($(option));
                $.each(data, function(key, value){
                    var option = new Option(value.title + " (" + value.type +")", value.pk);
                    new_placeholder.append($(option));
                });
            });

        });
    });

}) (django.jQuery);