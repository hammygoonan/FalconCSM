// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
(function($){

    $(document).foundation();
    $(document).ready(function(){
        if($('#content').length > 0){
            setInterval(function(){
                var text = $('#content').val();
                console.log(text);
                var converter = new Markdown.Converter();
                var html = converter.makeHtml(text);
                $('#preview').html(html);
            }, 1000);
        }
    });
})(jQuery);
