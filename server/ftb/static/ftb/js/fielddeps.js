
var ftb = {
    add_handle_dependent_field : function(dependent_on, dependent_element, dependent_value){
        var selected_value;
        if(dependent_on.is('select')){
            selected_value = dependent_on.find('option:selected').text();
        }
        dependent_element.attr('disabled', selected_value != dependent_value);
    }
};

function t1est(){alert('adf');} 

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
