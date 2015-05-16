String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

function autofill( evt ) {
    var val = $('#id_email').val();
    $('#id_username').val( val );
    var p = val.indexOf('.');
    var o = val.indexOf('@');
    if ( (p>0 && o == -1) ||  (p>0 && p<o) ) {
        $('#id_first_name').val(val.substr(0, p).capitalize());
        var o = val.indexOf('@');
        if ( o > 0 ) {
            $('#id_last_name').val(val.substr(p+1, o-p-1).capitalize());
            //$('#enterprise').val(val.substr( o+1 ));
        } else {
            $('#id_last_name').val(val.substr(p+1).capitalize());
        }
    } else {
        if (o > 0 ) {
            $('#id_first_name').val(val.substr(0, o).capitalize());
            $('#id_last_name').val("");
            //$('#enterprise').val(val.substr(o+1));
        } else {
            $('#id_first_name').val(val.capitalize());
            $('#id_last_name').val("");
        }
    }
}
$(document).ready(function() {
        $('#id_email').bind('change', autofill);
        $('#id_email').bind('keyup', autofill);
});
