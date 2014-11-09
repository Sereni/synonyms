<?php 
include('synonym_dictionary_1.php');
include('synonym_dictionary_2.php');
include('synonym_dictionary_3.php');
include('synonym_dictionary_4.php');
include('synonym_dictionary_5.php');
include('synonym_dictionary_6.php');
include('synonym_dictionary_7.php');
include('synonym_dictionary_8.php');
include('synonym_dictionary_9.php');
include('synonym_dictionary_10.php');
include('synonym_dictionary_11.php');
include('synonym_dictionary_12.php');
include('synonym_dictionary_13.php');
date_default_timezone_set('Europe/Moscow');

ini_set('memory_limit', '-1');

function print_synonym($dom, $syn)
{
	$syninfo = "";
	$syninfo .= "<a class=\"dom\">" . $dom . "</a>";
	if ($syn["mark"] != "")
	{
		$syninfo .= " " . $syn["mark"] . "[mark]";
	}
	$syninfo .= "<br>Ударение: " . $syn["stressed"];
	foreach($syn as $key => $value)
	{	
		if ($key == "stressed")
		{ continue; }
		$syninfo .= "<br>" . $key . ":<br>" . $value;
		
	}
	$syninfo .= "<br>";
	return $syninfo;
}

function find_synonym($input)
{	
	file_put_contents("./log.txt", $input . "\t[d_srch]\t" . date('d.m.Y H:i:s') . "\r\n", FILE_APPEND);
	if (array_key_exists($input, $GLOBALS['synonyms']))
	{
		$synrow = print_synonym($input, $GLOBALS['synonyms'][$input]);
		return $synrow;
	}
	else
	{
		$synrow = "Не найдено";
	}
	return $synrow;
}

function get_zones($zone)
{	
	$result = "";
	foreach($zone as $z)
	{
		$result .= $z . "/";
	}
	return rtrim($result, "/");
}

function complex_search($keywords, $zone)
{
	file_put_contents("./log.txt", $keywords . "\t{" . get_zones($zone) . "}\t" . date('d.m.Y H:i:s') . "\r\n", FILE_APPEND);
	if ($keywords == "")
	{
		return "Вы не указали ключевые слова"; 
	}
	if (is_null($zone))
	{ 
		return "Вы не выбрали зону поиска"; 
	}
	
	$result = array();
	
	#поиск по всем синонимам
	foreach($GLOBALS['synonyms'] as $dom => $syn)
	
	{	#по доминантам
		if (in_array("doms", $zone))
		{
			#echo $dom . " " . $keywords . "<br>";
			if(mb_strpos($dom, $keywords, 0, "utf-8") !== FALSE)
			{	
				$tuple[$dom] = $syn;
				array_push($result, $tuple);
				$tuple = array();
			}
		}
		
		#по остальным параметрам
		foreach($zone as $z)
		{	
			$flag = 1; #для того, чтобы не проверять еще одну зону, если нашлось по одной
			if ($z == "doms")
			{
				continue;
			}
			if (array_key_exists($z, $syn))
				{
					if(mb_strpos($syn[$z], $keywords, 0, "utf-8") !== FALSE)
					{
						$tuple[$dom] = $syn;
						array_push($result, $tuple);
						$tuple = array();
						$flag = 0;
						if (count($result) > 800)
						{
							
							return results_print($result);
							
						}
					}
				}
				if ($flag == 0)
					{ break; }
				
		}
	}
	if (count($result) == 0)
	{
		return "Данных не найдено";
	}
	return results_print($result);
}

function results_print($array)
{	
	$result = "";
	foreach($array as $i => $synrow)
	
	{	
		#echo $i . ": <br>";
		foreach($synrow as $dom => $syn)
		{
			#echo $dom . ": " . $syn . "<br>";
			$result .= print_synonym($dom, $syn) . "<hr>";
		}
	}
	return $result;
}

#$ar = array_unique(array_merge($ar1, $ar2, $ar3));

/*foreach($synonyms as $dom => $syn)
{
	echo print_synonym($dom, $syn);

}*/

#echo find_synonym("авантюрист");
#results_print(find_in_sense("Бабенко"));
?>