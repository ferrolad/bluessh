(function($) {
    $.jmessage_django = function(options) {
        var o = $.extend({}, $.jmessage_django.defaults, options);
            if(!$('.jbar').length){
                timeout = setTimeout('$.jmessage_django.removebar()',o.timeout);
                var _message_span = $(document.createElement('span'))
                        .addClass('jbar-content jbar-'+o.message_type).html(o.message);

                var _wrap_bar;
                (o.position == 'bottom') ? 
                _wrap_bar  = $(document.createElement('div')).addClass('jbar jbar-bottom'):
                _wrap_bar  = $(document.createElement('div')).addClass('jbar jbar-top') ;
                
                _wrap_bar.css({"background-color"	: o.background_color});
                if(o.removebutton){
                        var _remove_cross = $(document.createElement('a')).addClass('jbar-cross');
                        _remove_cross.click(function(e){$.jmessage_django.removebar();})
                }
                else{				
                        _wrap_bar.css({"cursor"	: "pointer"});
                        _wrap_bar.click(function(e){$.jmessage_django.removebar();})
                }	
                _wrap_bar.append(_message_span).append(_remove_cross).hide().appendTo($('body')).fadeIn('fast');
            }
    };

    $.jmessage_django.defaults = {
            background_color 	: '#FFFFFF',
            color		: '#000',
            message_type        : 'info',
            position	 	: 'top',
            removebutton     	: false,
            timeout	 	: 5000	
    };

    var timeout;
    $.jmessage_django.removebar = function(txt) {
            if($('.jbar').length){
                    clearTimeout(timeout);
                    $('.jbar').fadeOut('fast',function(){
                            $(this).remove();
                    });
            }	
    };
	
})(jQuery);
