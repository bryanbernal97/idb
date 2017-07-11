<!DOCTYPE html>
<html lang="EN">
<head>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Search Engine</title>
</head>

<body>

<center>
<form action"./results.php" method="get">
	<input type="text" name="input" size="50" <?php echo $_GET ['input']; ?> />

	<input type="submit" value="search" />

</form>
</center>

<?php
	$input = $_GET['input'];
	$terms = explode(" "), $input);
	$query = "SELECT * FROM search WHERE ";

	foreach ($terms as $each) {
		$i++;
		if ($i == 1)
			$query .= "keywords LIKE '%each%' ";
		else
			$query .= "OR keywords LIKE '%each%' ";
	}

	//Connect to Database
	mysql_connect("localhost", "", "");
	mysql_select_db("name of db");
	$query = mysql_query($query);
	$numrows = mysql_num_rows($query);
	if($numrows > 0){
		while ($rows = mysqlfetch_assoc($query)){
		<!-- get id field from db -->
			$id = $row['id'];
			$title = $row['title'];
			$description = $row['description'];
			$link = $row['link'];
			<!-- ... -->

			echo "<h2><a href='$link'>$title</a></h2>$description<br/><br/>";


		}
	}

	else 
		echo "No results found for \"<b>$input</b>\"";

	//Disconnect
	mysql_close();
?>

</body>
</html>