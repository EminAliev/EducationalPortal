function formValidation()
{
var passid = document.registration.passid;
var uname = document.registration.username;
var uemail = document.registration.email;
if(passid_validation(passid,7,12))
{
if(allLetter(uname))
{ 
if(ValidateEmail(uemail))
{
{
}
} 
}
} 
return false;
}

function allLetter(uname)
{ 
var letters = /^[A-Za-z]+$/;
if(uname.value.match(letters))
{
return true;
}
else
{
alert('Username must have alphabetcharactersonly');
uname.focus();
return false;
}
}




function alphanumeric(uadd)
{ 
var letters = /^[0-9a-zA-Z]+$/;
if(uadd.value.match(letters))
{
return true;
}
else
{
alert('User address must have alphanumericcharactersonly');
uadd.focus();
return false;
}
}


function passid_validation(passid,mx,my)
{
var passid_len = passid.value.length;
if (passid_len == 0 ||passid_len>= my || passid_len<mx)
{
alert("Password should not be empty / length be between "+mx+" to "+my);
passid.focus();
return false;
}
return true;
}


function userid_validation(uid,mx,my)
{
var uid_len = uid.value.length;
if (uid_len == 0 || uid_len>= my || uid_len<mx)
{
alert("User Id should not be empty / length be between "+mx+" to "+my);
uid.focus();
return false;
}
return true;
}

function ValidateEmail(uemail)
{
var mailformat = /^w+([.-]?w+)*@w+([.-]?w+)*(.w{2,3})+$/;
if(uemail.value.match(mailformat))
{
return true;
}
else
{
alert("You have entered an invalid email address!");
uemail.focus();
return false;
}
}
