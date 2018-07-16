<html>
<a href="index.php">Homepage</a>
<a href="?page=register">Free register</a></li>

<?php
if(isset($_GET["page"]) && !empty($_GET["page"])) {
    $page = $_GET["page"];
    if(strpos(strtolower($page), 'secret') !== false) {
        die('No no no!');
    }
//    else if(strpos($page, 'php') !== false) {
 //       die("N0 n0 n0!");
//    }
    else {
        include($page . '.php');
    }
}
?>
</html>
