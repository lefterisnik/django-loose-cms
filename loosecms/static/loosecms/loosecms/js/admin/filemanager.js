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


        /******************************Open upload or select dialog***********************************/

        $('body').on('click', '.filemanager', function(e){
            e.preventDefault();
            select_field_id = $(this).data('id');
            path = $(this).data('path');

            var name = "UploadWindow";
            var href = $(this).attr('href');
            var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
            win.focus();
            return false;
        });
    });

}) (django.jQuery);
