function bindEvents() {

$('#loader1').hide();
//$('#loader2').hide();
$('form').bind("submit",submitClicked);
//$('#signup').bind('click',signupClicked);

}

function submitClicked()
{
    status = validatePassword();
    if (status == 1)
    {
        $('#loader1').show();
//        $('#loader2').show();
        return true;
    }
    else
    {
        return false;
    }
}



function validatePassword(){
  var password = document.getElementById("txtPassword"), confirm_password = document.getElementById("confirmtxtPassword");

  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
    return 0;
  } else {
    confirm_password.setCustomValidity('');
    return 1;
  }
}

