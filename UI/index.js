function validateFields()
{
    var name = document.getElementById("Name").value;
    var email = document.getElementById("Email").value;
    var password = document.getElementById("Password").value;
    var reenterpassword = document.getElementById("ReEnterPassword").value;

    if (name.length >= 4 && validatePassword(password, reenterpassword) && validateEmail(email))
    {
        $.post("http://127.0.0.1:5000/register", 
               {"name":name,
               "email":email,
               "password":password},
               //callback function
              function(data, status){
                if (status === "success")
                {
                    document.getElementById("result").innerHTML = data.message;        
                }
        });
    }
    else
    {
        document.getElementById("result").innerHTML = "Please check the fields."
    }
}

function validatePassword(pass1, pass2)
{
    if (pass1 === pass2 && (pass1.length >= 6 && pass1.length <= 15))
    {
        return true;
    }
    return false;
}

function validateEmail(email) 
{
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function validateLogin()
{
    if (validateEmail(document.getElementById("Email").value))
    {
        $.post("http://127.0.0.1:5000/login",
              {"email":document.getElementById("Email").value,
              "password":document.getElementById("Password").value},
              function(data, status){
                  console.log(status);
                  if (status === "success")
                  {
                      document.getElementById("result").innerHTML = 
                          data.message;
                  }
              });
    }
    else
    {
        document.getElementById("result").innerHTML = "Invalid ID and Password combination.";
    }
}

function handleTransTypeOnChange()
{
    var selected = document.getElementById("tranType");
    if (selected.selectedIndex === 1)
    {
        document.getElementById("inc").style.display = "none";
        document.getElementById("exp").style.display = "inline-block";
    }
    else
    {
        document.getElementById("inc").style.display = "inline-block";
        document.getElementById("exp").style.display = "none";
    }
}

function recordTransaction()
{
    var title = document.getElementById("title").value;
    var amount = document.getElementById("amount").value;
    var tranType;
    var catType;
    if (title != "" && amount != "")
    {
        var transactionType = document.getElementById("tranType").value;
        if(transactionType == "income")
        {
            tranType = "income";
            catType = document.getElementById("inc").value;
        }
        else
        {
            tranType = "expense";
            catType = document.getElementById("exp").value;
        }
        var description = document.getElementById("description").value;
        var date = document.getElementById("date").value;
        $.post("http://127.0.0.1:5000/recordTransaction",{
            "transaction_type":tranType,
            "category":catType,
            "title":title,
            "description":description,
            "amount":amount
            //TO DO Handle date logic (server side)
        }, function (data, response) {
            document.getElementById("result").innerHTML = data["message"];
        });
    }
    else
    {
        document.getElementById("result").innerHTML = "Required fields cannot be empty.";
    }
}