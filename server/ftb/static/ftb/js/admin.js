var ftb_admin = {
    assign_date_picker_widget : function(){
        $('.vDateField').datepicker({ dateFormat: 'yy-mm-dd' });
    }
};

(function($){
    $(document).ready(ftb_admin.assign_date_picker_widget)
})(django.jQuery)

