function bindEvents() {

$('#loader1').hide();
//$('#loader2').hide();
$('form').bind("submit",submitClicked);
//$('#signup').bind('click',signupClicked);

}

function submitClicked()
{
    $('#loader1').show();
    $('#loader2').show();
    return true;

}


