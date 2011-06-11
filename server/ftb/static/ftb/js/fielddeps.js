
var ftb = {
    add_handle_dependent_field : function(dependent_on, dependent_element, dependent_value){
        var selected_value;
        if(dependent_on.is('select')){
            selected_value = dependent_on.find('option:selected').text();
        }
        if(!dependent_on.attr('disabled' && selected_value == dependent_value){
            dependent_element.attr('disabled', false);
        }else {
            ftb.set_none(dependent_element);
            dependent_element.attr('disabled', true);
        }
    },
    set_none : function(element){
        if(element.is('select')){
            element.val(element.find('option:selected'));
        }else if(element.is('input')){
            element.val(null);
        }
    }
    
    
};

(function($){
    $(document).ready(function(){
        $('*[class*="depends_on-"]').not('[class*="_prefix_"]').each(
            function(index){
                var dependent = $(this)
                dependent_name_and_value = $(this).attr('class').match(/depends_on-(.*)-with_value-(.*)/)
                var dependent_on = $('*[id$="' + dependent_name_and_value[1] + '"]').not('[id*="_prefix_"]')
                dependent_on.change(function(){
                    ftb.add_handle_dependent_field($(this), dependent, dependent_name_and_value[2]);
                });
                ftb.add_handle_dependent_field(dependent_on, dependent, dependent_name_and_value[2]);
            }
        )
    })
})(django.jQuery)
