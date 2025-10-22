#!/bin/bash
# Test hash verification

docker exec mailcowdockerized-php-fpm-mailcow-1 php <<'PHPEOF'
<?php
$stored_hash = '{BLF-CRYPT}$2b$10$4fSyUgoV2o/28ALBkPhKWuYrd/lA..CeW6GviQrCJwoCyrfaWicuy';
$password = 'Admin2025!';

// Extract the hash part
$parts = explode('}', $stored_hash);
echo "Stored: " . $stored_hash . "\n";
echo "Scheme: " . $parts[0] . "\n";
echo "Hash part: " . $parts[1] . "\n";

// Test verification
$result = password_verify($password, $parts[1]);
echo "Verify result: " . ($result ? 'OK' : 'FAIL') . "\n";
?>
PHPEOF
