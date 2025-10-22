<?php
$password = "Admin2025!";
$hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 10]);
echo "Generated hash: " . $hash . "\n";
echo "Hash length: " . strlen($hash) . "\n";
echo "Verify test: " . (password_verify($password, $hash) ? "OK" : "FAIL") . "\n";
?>
