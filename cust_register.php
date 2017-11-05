
<!DOCTYPE HTML>  
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body>  


<h2>Customer Form Validation Example</h2>
<p><span class="error">* required field.</span></p>
<form method="post" action="cust_register_back.php">  
  First Name: <input type="text" name="fname" >
  
  <br><br>
  Last Name: <input type="text" name="lname" >
  
  <br><br>
  E-mail: <input type="text" name="email" >
  
  <br><br>
  Gender: <input type="text" name="gender" >
  
  <br><br>
  <input type="submit" name="submit" value="Submit">  
</form>


</body>
</html>
