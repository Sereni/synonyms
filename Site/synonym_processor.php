<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<link  type="text/css" rel="stylesheet" href="syn_styles.css">
</head>
<body>
<?php
	include('synonym_functions.php');
	echo "<h3>Результат:</h3><hr>";
	if ($_POST["dominant"] != "")
	{
		echo find_synonym($_POST["dominant"]);
	}
	else
	{
		echo complex_search($_POST["keywords"], $_POST["zone"]);
	}
?>
</font>
</body>
</html>
