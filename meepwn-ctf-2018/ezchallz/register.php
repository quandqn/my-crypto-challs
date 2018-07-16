<html>
<?php
error_reporting(0);

function gendirandshowflag($username) {
	include('secret.php');
	$dname = "";
	$intro = "";
	$_username = md5($username, $raw_output = TRUE);
	for($i = 0; $i<strlen($salt); $i++) {
		$dname.= chr(ord($salt[$i]) ^ ord($_username[$i]));
	};
	$dname = "users/" . bin2hex($dname);
	echo 'You have successfully register as ' . $username . '!\n';
	if ($_username === hex2bin('21232f297a57a5a743894a0e4a801fc3')) {
		$intro = "Here is your flag:" . $flag;
	}
	else {
		$intro = "Here is your flag, but I'm not sure 🤔: \nMeePwnCTF{" . md5(random_bytes(16) . $username) . "}";
	}
	mkdir($dname);
	file_put_contents($dname . '/flag.php', $intro);
	header("Location: ". $dname . "/flag.php");
}

if (isset($_POST['username'])) {
	if ($_POST['username'] === 'admin') {
		die('Username is not allowed!');
	}
	else {
		gendirandshowflag($_POST['username']);
	}
}
?>

        <form action="?page=register" method="POST">
        <input type="text" name="username"><br>
        <input type="submit" value="Register">
        </form>
</html>

